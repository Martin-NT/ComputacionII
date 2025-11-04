# Módulo encargado de la descarga asíncrona del contenido HTML.
from __future__ import annotations
import aiohttp # Librería HTTP asíncrona
from typing import Optional

# Configuración por defecto de la sesión HTTP

# Timeout total de 30 segundos para cada solicitud (evita bloqueos).
DEFAULT_TIMEOUT = aiohttp.ClientTimeout(total=30)

# Encabezado User-Agent personalizado (buena práctica en scraping).
DEFAULT_HEADERS = {"User-Agent": "TP2-Scraper/1.0 (+https://um.edu.ar)"}

# Recibe: una URL a descargar.
async def fetch_text(url: str, *, headers: Optional[dict] = None) -> str:
    # Mezclamos encabezados por defecto con los opcionales.
    merged = {**DEFAULT_HEADERS, **(headers or {})}

    # Abrimos una sesión HTTP asíncrona.
    async with aiohttp.ClientSession(timeout=DEFAULT_TIMEOUT, headers=merged) as session:
        # Hacemos la solicitud GET. allow_redirects=True permite seguir redirecciones.
        async with session.get(url, allow_redirects=True) as resp:
            # Si el servidor devuelve un código de error (4xx/5xx), lanza excepción.
            resp.raise_for_status()
            # Devolvemos el cuerpo HTML como texto (ya decodificado).
            return await resp.text()
