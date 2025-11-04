# server_scraping.py - Servidor Asíncrono 
from __future__ import annotations
import argparse                      
import asyncio                            
from datetime import datetime, timezone   
from typing import Dict, Any
from aiohttp import web              
from scraper.async_http import fetch_text 
from scraper.html_parser import parse_html     
from scraper.metadata_extractor import extract_meta 
from common.serialization import to_json, from_json 

# 1: Protocolo de comunicación A ↔ B (TCP binario)

# Enviamos el mensaje con prefijo de longitud (4 bytes) + JSON codificado
async def send_len_prefixed(writer: asyncio.StreamWriter, payload: bytes) -> None:
    writer.write(len(payload).to_bytes(4, "big") + payload)
    await writer.drain()

# Leemos exactamente N bytes del socket (bloque de lectura seguro)
async def recv_exact(reader: asyncio.StreamReader, n: int) -> bytes:
    buf = bytearray()
    while len(buf) < n:
        chunk = await reader.read(n - len(buf))
        if not chunk:
            raise ConnectionError("socket closed during recv_exact")
        buf.extend(chunk)
    return bytes(buf)

# Recibimos un mensaje completo con prefijo de longitud
async def recv_len_prefixed(reader: asyncio.StreamReader) -> bytes:
    length_b = await recv_exact(reader, 4)
    length = int.from_bytes(length_b, "big")
    return await recv_exact(reader, length)


# 2: Comunicación asíncrona con el Servidor B

async def call_processing_server_async(host: str, port: int, payload: Dict[str, Any], *, timeout: float = 10.0) -> Dict[str, Any]:
    """
    Abre una conexión TCP con el servidor de procesamiento (B),
    envía una petición JSON y espera una respuesta JSON.
    Se hace de forma asíncrona (sin bloquear el event loop).
    """
    async def _roundtrip() -> Dict[str, Any]:
        # Abre una conexión TCP asíncrona
        reader, writer = await asyncio.open_connection(host=host, port=port)
        try:
            # Envía datos al servidor B
            await send_len_prefixed(writer, to_json(payload))
            # Espera la respuesta completa
            raw = await recv_len_prefixed(reader)
            # Devuelve el JSON decodificado
            return from_json(raw)
        finally:
            # Cierra la conexión
            writer.close()
            await writer.wait_closed()

    # Aplica timeout general de comunicación
    return await asyncio.wait_for(_roundtrip(), timeout=timeout)



# 3: Handler principal del servidor HTTP

async def handle_scrape(request: web.Request) -> web.Response:
    """
    Endpoint principal: /scrape?url=<sitio>
    - Recibe una URL
    - Lanza tareas asíncronas:
        1) Descarga del HTML (scraping)
        2) Comunicación con el servidor B (procesamiento)
    - Extrae información del HTML
    - Devuelve JSON consolidado (scraping + processing)
    """

    # Validación de parámetros 
    url = request.rel_url.query.get("url")
    print(f"\n[Servidor A] Recibida petición para: {url}")
    if not url:
        return web.json_response({"status": "error", "error": "missing url"}, status=400)
    
    # Usa el semáforo guardado en la app
    async with request.app["semaphore"]:
        try:
            # Ejecución de tareas en paralelo 
            # 1) Descargar HTML
            fetch_task = asyncio.create_task(fetch_text(url))
            # 2) Enviar trabajo al servidor B (procesamiento)
            proc_task = asyncio.create_task(
                call_processing_server_async(request.app["proc_ip"], request.app["proc_port"], {"url": url})
            )

            # Espera a que termine la descarga del HTML
            html = await fetch_task

            # Procesamiento local del HTML
            parsed = parse_html(html, url) # Título, links, headers, imágenes
            meta = extract_meta(html) # Metadatos relevantes
            scraping_data = {**parsed, "meta_tags": meta}

            # Espera la respuesta del servidor B 
            processing_data = {}
            try:
                proc_resp = await proc_task
                processing_data = proc_resp.get("processing_data", {})
            except Exception:
                # Si B no está disponible, seguimos sin romper el flujo
                processing_data = {}

            # Construcción del JSON final 
            out = {
                "url": url,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "scraping_data": scraping_data,
                "processing_data": processing_data,
                "status": "success",
            }

            # Devuelve respuesta JSON
            print(f"[Servidor A] Tarea completada para: {url}")
            return web.json_response(out)

        # Manejo de errores globales 
        except asyncio.TimeoutError:
            # Si se agota el tiempo de espera
            return web.json_response({"status": "error", "error": "timeout"}, status=504)
        except Exception as e:
            # Cualquier otro error inesperado
            return web.json_response({"status": "error", "error": str(e)}, status=500)


# 4: Inicialización de la aplicación aiohttp

async def make_app(proc_ip: str, proc_port: int, max_workers: int) -> web.Application:
    """
    Crea la aplicación aiohttp, define rutas y variables globales.
    """
    app = web.Application()
    # Configuración para hablar con el servidor B
    app["proc_ip"] = proc_ip
    app["proc_port"] = proc_port

    # Límite de concurrencia (rate limiting / control de carga)
    app["semaphore"] = asyncio.Semaphore(max_workers)

    # Ruta principal
    app.router.add_get("/scrape", handle_scrape)
    return app


# 5: CLI y punto de entrada principal

def main():
    """
    Configura el CLI, inicia el servidor HTTP y lo deja escuchando.
    """
    parser = argparse.ArgumentParser(
        description="Servidor de Scraping Web Asíncrono (Parte A)"
    )

    parser.add_argument(
        "-i", "--ip",
        default="0.0.0.0",
        help="Dirección de escucha (IPv4/IPv6)"
    )

    parser.add_argument(
        "-p", "--port",
        type=int,
        default=8000,
        help="Puerto de escucha HTTP"
    )

    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=4,
        help="Número máximo de scrapes concurrentes (default: 4)"
    )

    parser.add_argument(
        "--proc-ip",
        required=True,
        help="Dirección IP del servidor de procesamiento (B)"
    )

    parser.add_argument(
        "--proc-port",
        type=int,
        required=True,
        help="Puerto del servidor de procesamiento (B)"
    )

    args = parser.parse_args()

    # Inicia la aplicación aiohttp (servidor asíncrono)
    web.run_app(
        make_app(args.proc_ip, args.proc_port, args.workers),
        host=args.ip,
        port=args.port,
        reuse_port=True,
    )


if __name__ == "__main__":
    main()
