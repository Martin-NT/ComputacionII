# Encargado de extraer los metadatos relevantes de una página HTML.
from __future__ import annotations
from bs4 import BeautifulSoup

# Conjunto de meta tags relevantes que se quiere extraer del HTML.
RELEVANT_META = {
    "description",
    "keywords",
    "og:title",
    "og:description",
    "og:image",
}

# Recibe: el HTML completo de una página.
def extract_meta(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")  # Se usa lxml por su rapidez y tolerancia
    meta = {}

    # Iteramos todas las etiquetas <meta> del documento
    for tag in soup.find_all("meta"):
        # name puede venir como 'name' o 'property' (por Open Graph)
        name = (tag.get("name") or tag.get("property") or "").strip().lower()
        # El contenido del meta
        content = (tag.get("content") or "").strip()

        # Si el meta está en los relevantes y tiene contenido, lo guardamos
        if name in RELEVANT_META and content:
            meta[name] = content

    return meta 
