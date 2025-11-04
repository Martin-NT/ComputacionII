# Cliente HTTP de prueba para el SERVIDOR A
# Imprime el JSON completo Y guarda el screenshot.
import requests
import base64
import json 

# Configuración
SERVER_URL = "http://127.0.0.1:8000/scrape"
URL_TO_SCRAPE = "https://example.com"  # URL fija para la prueba
OUTPUT_IMAGE = "screenshot_cliente.png"

print(f"--- Prueba Completa: Analizando {URL_TO_SCRAPE} ---")

try:
    # 1. Hacer la petición GET al Servidor A
    params = {'url': URL_TO_SCRAPE}
    resp = requests.get(SERVER_URL, params=params, timeout=30)
    
    # Verificar si la petición HTTP fue exitosa
    resp.raise_for_status() 
    
    # 2. Convertir la respuesta a JSON
    data = resp.json()

    # --- TAREA 1: Imprimir el JSON ---
    print("\n--- JSON Recibido del Servidor A: ---")
    # Usamos json.dumps para formatear el JSON con indentación
    print(json.dumps(data, indent=4, ensure_ascii=False))
    print("--------------------------------------\n")

    # --- TAREA 2: Guardar la Imagen ---
    if data.get("status") == "success":
        print("Procesando y guardando screenshot...")
        
        # Extraer, decodificar y guardar
        img_b64 = data['processing_data']['screenshot']
        img_data = base64.b64decode(img_b64)
        
        with open(OUTPUT_IMAGE, "wb") as f:
            f.write(img_data)
        
        # Imprimir mensaje de éxito
        print(f"✅ ¡Imagen guardada como {OUTPUT_IMAGE}!")

    else:
        print(f"Error en la respuesta del servidor: {data.get('error')}")

except requests.exceptions.RequestException as e:
    print(f"\n❌ ERROR: No se pudo conectar al servidor A ({SERVER_URL})")
    print("Asegúrate de que 'server_scraping.py' esté corriendo.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")