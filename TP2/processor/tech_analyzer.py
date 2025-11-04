# Opción 3: Análisis Avanzado de Tecnologías Web
import warnings 
from Wappalyzer import Wappalyzer, WebPage
from typing import Dict, Any

def analyze_technologies(url: str) -> Dict[str, Any]:
    """
    Analiza una URL para detectar las tecnologías web que utiliza.
    """
    print(f"[Procesador] Analizando tecnologías para: {url}")
    try:
        # Wappalyzer (y sus dependencias) generan avisos (UserWarning) que no podemos controlar. Los ocultamos para limpiar la salida.
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            
            # Este código ahora corre con los avisos silenciados:
            wappalyzer = Wappalyzer.latest()
            webpage = WebPage.new_from_url(url, timeout=10)
            tech_info = wappalyzer.analyze_with_categories(webpage)

        # Simplifica el resultado para el JSON
        result = {}
        for category, apps in tech_info.items():
            result[category] = list(apps.keys()) # Devuelve solo los nombres
            
        return result
    
    except Exception as e:
        print(f"[ADVERTENCIA] Análisis de tecnología falló para {url}. Error: {e}")
        return {"error": str(e)}