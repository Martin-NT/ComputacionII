#server_processing.py
from __future__ import annotations
import argparse
import socketserver
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from typing import Any, Dict

# Tu serialización y helpers (se mantienen)
from common.serialization import to_json, from_json

# === Protocolo binario length-prefixed (se mantiene tu estilo) ===
def recv_exact(sock, n: int) -> bytes:
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("socket closed")
        buf.extend(chunk)
    return bytes(buf)

def recv_msg(sock) -> bytes:
    length = int.from_bytes(recv_exact(sock, 4), "big")
    return recv_exact(sock, length)

def pack_msg(payload: bytes) -> bytes:
    return len(payload).to_bytes(4, "big") + payload


# === Import de funciones de procesamiento ===
# Si aún no tenés los módulos, estos fallbacks permiten probar el server.
try:
    from processor.screenshot import take_screenshot
except Exception:
    def take_screenshot(url: str) -> str:
        # Fallback: devuelve un PNG base64 "dummy" (imagen 1x1)
        import base64
        return base64.b64encode(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
                                b"\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde"
                                b"\x00\x00\x00\x0cIDATx\x9cc``\x00\x00\x00\x02\x00\x01\xe2!\xbc3"
                                b"\x00\x00\x00\x00IEND\xaeB`\x82").decode("ascii")

try:
    from processor.performance import analyze_performance
except Exception:
    def analyze_performance(url: str) -> Dict[str, int]:
        # Fallback mínimo para no romper
        return {"load_time_ms": 0, "total_size_kb": 0, "num_requests": 1}

try:
    from processor.image_processor import generate_thumbnails
except Exception:
    def generate_thumbnails(url: str, *, max_images: int = 3, thumb_size=(240, 240)) -> list[str]:
        # Fallback sin thumbnails
        return []


# === Worker que corre en proceso ===
def process_website(url: str, *, thumb_count: int = 3, thumb_size=(240, 240)) -> Dict[str, Any]:
    screenshot_b64 = take_screenshot(url)
    performance = analyze_performance(url)
    thumbnails = generate_thumbnails(url, max_images=thumb_count, thumb_size=thumb_size)
    return {
        "screenshot": screenshot_b64,
        "performance": performance,
        "thumbnails": thumbnails,
    }


# === Handler del servidor (hilo por conexión) ===
class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            raw = recv_msg(self.request)
            req = from_json(raw)  # puede ser {"url": "..."} o {"task":"analyze","url":"...","options":{...}}

            # Compatibilidad con tu prueba anterior
            url = req.get("url")
            if not url:
                raise ValueError("missing 'url' in request")

            options = req.get("options", {})
            thumb_count = int(options.get("thumb_count", 3))
            thumb_size = tuple(options.get("thumb_size", (240, 240)))

            # Ejecutar en proceso del pool
            future = self.server.executor.submit(
                process_website, url, thumb_count=thumb_count, thumb_size=thumb_size
            )
            result = future.result()  # Este hilo espera, pero el CPU pesado va en procesos

            resp = {"status": "ok", "processing_data": result}
            self.request.sendall(pack_msg(to_json(resp)))


        except Exception as exc:
            err = {"status": "error", "error": str(exc)}
            self.request.sendall(pack_msg(to_json(err)))



# === Servidor TCP con hilos ===
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    # inyectamos .executor en main()


def main():
    p = argparse.ArgumentParser(description="Servidor de Procesamiento Distribuido (Parte B)")
    p.add_argument("-i", "--ip", required=True, help="Dirección de escucha")
    p.add_argument("-p", "--port", type=int, required=True, help="Puerto de escucha")
    p.add_argument("-n", "--processes", type=int, default=mp.cpu_count(),
                   help="Número de procesos del pool (default: CPU count)")
    args = p.parse_args()

    with ProcessPoolExecutor(max_workers=args.processes) as executor:
        ThreadedTCPServer.executor = executor
        with ThreadedTCPServer((args.ip, args.port), Handler) as srv:
            print(f"[B] listening on {args.ip}:{args.port} (pool={args.processes})")
            try:
                srv.serve_forever()
            except KeyboardInterrupt:
                print("\n[B] shutting down…")


if __name__ == "__main__":
    main()
