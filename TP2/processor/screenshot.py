# Captura de pantalla de una página web.
# Intenta usar Playwright (Chromium headless) para obtener un screenshot real.
# Si falla por cualquier motivo (no está instalado chromium de playwright, etc.),
# usa un placeholder generado con Pillow.
# Siempre devuelve un string base64 (PNG) listo para serializar en JSON.
import base64
import io
from PIL import Image, ImageDraw

def _placeholder_image(url: str) -> str:
    """
    Fallback: genera una imagen PNG sintética que incluye la URL.
    Esto garantiza que el servidor B siempre devuelva algo válido,
    incluso si no hay navegador headless disponible en el entorno.
    """
    width, height = 1280, 720
    img = Image.new("RGB", (width, height), color=(245, 247, 250))
    draw = ImageDraw.Draw(img)

    draw.text((40, 40), "Placeholder de Screenshot", fill=(30, 30, 30))
    draw.text((40, 100), f"URL: {url}", fill=(60, 60, 60))
    
    draw.rectangle(
        [(20, 20), (width - 20, height - 20)],
        outline=(200, 200, 200),
        width=2
    )

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")

def _screenshot_playwright(url: str) -> bytes:
    """
    Usa Playwright para abrir Chromium en modo headless,
    navegar a la URL y capturar un screenshot de la página.
    Devuelve los bytes PNG crudos (no base64 todavía).

    Si algo falla, levanta excepción para que el caller decida fallback.
    """
    from playwright.sync_api import sync_playwright

    # Playwright maneja el browser y el driver internamente.
    # No necesitamos Chrome del sistema ni chromedriver.
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": 1280, "height": 720}
        )

        # timeout en ms para la navegación
        page.goto(url, timeout=15000)  # 15 segundos máximo

        # screenshot de la página completa (full_page=True) o solo viewport
        png_bytes = page.screenshot(full_page=True)

        browser.close()

    return png_bytes

def take_screenshot(url: str) -> str:
    """
    Devuelve SIEMPRE un PNG en base64.

    1. Intenta screenshot real con Playwright headless (Chromium controlado).
    2. Si falla, vuelve al placeholder generado con Pillow.

    Esta función es llamada por el servidor B dentro de un worker de multiprocessing.
    """
    try:
        png_bytes = _screenshot_playwright(url)
        return base64.b64encode(png_bytes).decode("ascii")

    except Exception as e:
        print(f"[ADVERTENCIA] Screenshot (Playwright) falló para {url}. Usando placeholder. Error: {e}")
        return _placeholder_image(url)