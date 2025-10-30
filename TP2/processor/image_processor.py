# processor/image_processor.py
# Descarga imágenes y genera thumbnails en base64

import base64, io, requests
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import urljoin

REQ_TIMEOUT = 15

def _download_image(url):
    try:
        r = requests.get(url, timeout=REQ_TIMEOUT, stream=True)
        r.raise_for_status()
        return Image.open(io.BytesIO(r.content)).convert("RGB")
    except Exception:
        return None

def _b64_of_image(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")

def generate_thumbnails(url, *, max_images=3, thumb_size=(240, 240)):
    try:
        html = requests.get(url, timeout=REQ_TIMEOUT).text
    except Exception:
        return []

    soup = BeautifulSoup(html, "lxml")
    img_srcs = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if not src: continue
        if src.startswith("//"): src = "https:" + src
        elif src.startswith("/"): src = urljoin(url, src)
        img_srcs.append(src)
        if len(img_srcs) >= max_images: break

    thumbs = []
    for src in img_srcs:
        im = _download_image(src)
        if im is None: continue
        im.thumbnail(thumb_size)
        thumbs.append(_b64_of_image(im))
    return thumbs
