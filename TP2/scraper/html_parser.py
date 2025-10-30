# scraper/html_parser.py
# Módulo encargado de analizar (parsear) el HTML descargado.
from __future__ import annotations
from bs4 import BeautifulSoup       # Librería para parsear HTML de forma sencilla
from collections import Counter     # Para contar cantidad de etiquetas
from urllib.parse import urljoin    # Para convertir URLs relativas en absolutas

def parse_html(html: str, base_url: str) -> dict:
    # Creamos el árbol de análisis con lxml (rápido y tolerante a errores)
    soup = BeautifulSoup(html, "lxml")

    # Extrae título de la página
    # Si la etiqueta <title> existe, tomamos su texto y eliminamos espacios. Si no existe, devolvemos None.
    title = (soup.title.string.strip() if soup.title and soup.title.string else None)

    # Extrae todos los enlaces (<a href="...">)
    #   Busca todas las etiquetas <a> con atributo href.
    #   Convierte los enlaces relativos en absolutos con urljoin(base_url, href).
    links = []
    for a in soup.find_all("a", href=True):
        href = a.get("href").strip()
        links.append(urljoin(base_url, href))  # Convierte /path a https://dominio/path

    # Contar encabezados (estructura de la página)
    #   Creamo un contador con claves h1..h6.
    #   Para cada nivel, cuenta cuántas etiquetas hay.
    headers = Counter({f"h{i}": 0 for i in range(1, 7)})
    for i in range(1, 7):
        headers[f"h{i}"] = len(soup.find_all(f"h{i}"))

    # Cuenta la cantidad de imágenes (<img>)
    images_count = len(soup.find_all("img"))

    # Devuelve los resultados en un diccionario estructurado
    return {
        "title": title,               
        "links": links,                # Lista de enlaces absolutos
        "structure": dict(headers),    # Cantidad de headers h1..h6
        "images_count": images_count,  
    }
