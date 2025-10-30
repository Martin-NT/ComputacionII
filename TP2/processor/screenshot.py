# processor/screenshot.py
# Genera un “screenshot” de la página (placeholder si no se usa Selenium)
import base64
import io
from PIL import Image, ImageDraw

def take_screenshot(url: str) -> str:
    # --- Crea imagen simulada con texto ---
    width, height = 1280, 720
    img = Image.new("RGB", (width, height), color=(245, 247, 250))
    draw = ImageDraw.Draw(img)
    draw.text((40, 40), "Screenshot Placeholder", fill=(30, 30, 30))
    draw.text((40, 100), url, fill=(60, 60, 60))
    draw.rectangle([(20, 20), (width - 20, height - 20)], outline=(200, 200, 200), width=2)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")
