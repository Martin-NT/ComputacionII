# Calcula tiempos y tamaños de carga de la página
import time
import math
import requests
from bs4 import BeautifulSoup

MAX_IMAGES = 5
REQ_TIMEOUT = 15

def _safe_head_or_get(url: str) -> int:
    """Descarga segura para medir tamaño"""
    try:
        r = requests.head(url, timeout=REQ_TIMEOUT, allow_redirects=True)
        cl = r.headers.get("Content-Length")
        if cl: return int(cl)
    except Exception:
        pass
    try:
        r = requests.get(url, timeout=REQ_TIMEOUT, stream=True)
        size = sum(len(c) for c in r.iter_content(64 * 1024))
        return size
    except Exception:
        return -1

def analyze_performance(url: str) -> dict:
    """Calcula load_time, total_size_kb y num_requests"""
    t0 = time.perf_counter()
    resp = requests.get(url, timeout=REQ_TIMEOUT)
    html_size = len(resp.content)
    load_time_ms = int((time.perf_counter() - t0) * 1000)

    soup = BeautifulSoup(resp.text, "lxml")
    img_urls = []
    for tag in soup.find_all("img"):
        src = tag.get("src")
        if not src: continue
        if src.startswith("//"): src = "https:" + src
        elif src.startswith("/"):
            from urllib.parse import urljoin
            src = urljoin(url, src)
        img_urls.append(src)
        if len(img_urls) >= MAX_IMAGES: break

    total_bytes = html_size
    successful = 0
    for img in img_urls:
        sz = _safe_head_or_get(img)
        if sz > 0:
            total_bytes += sz
            successful += 1

    return {
        "load_time_ms": load_time_ms,
        "total_size_kb": int(math.ceil(total_bytes / 1024)),
        "num_requests": 1 + successful,
    }
