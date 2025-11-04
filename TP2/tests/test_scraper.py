# Prueba de integración para el Servidor A (Scraping)
import asyncio
import aiohttp
import sys

# La URL del Servidor A
SERVER_URL = "http://localhost:8000/scrape"
TEST_URL = "https://example.com"

async def test_scraper():
    """
    Prueba el sistema completo a través del Servidor A (server_scraping.py)
    """
    print("Iniciando prueba del Servidor A (Scraping)...")
    try:
        async with aiohttp.ClientSession() as session:
            
            # Hacemos la petición al endpoint /scrape
            print(f"Enviando petición a {SERVER_URL}?url={TEST_URL}...")
            async with session.get(f'{SERVER_URL}?url={TEST_URL}', timeout=20) as resp:
                
                # 1. Verificar que el servidor respondió OK (código 200)
                assert resp.status == 200, f"Error, el servidor respondió con: {resp.status}"
                
                data = await resp.json()
                
                # 2. Verificar que la respuesta tiene la estructura esperada
                assert 'status' in data, "Respuesta JSON no tiene 'status'"
                assert data['status'] == 'success', "El status de la operación no fue 'success'"
                
                # 3. Verificar que AMBOS servidores contribuyeron
                assert 'scraping_data' in data, "Respuesta JSON no tiene 'scraping_data' (Falla Servidor A)"
                assert 'processing_data' in data, "Respuesta JSON no tiene 'processing_data' (Falla Servidor A o B)"
                
                # 4. Verificar datos clave del Servidor A
                assert data['scraping_data']['title'] == 'Example Domain', "El título extraído es incorrecto"
                
                # 5. Verificar datos clave del Servidor B
                assert 'screenshot' in data['processing_data'], "No se encontró el screenshot en processing_data"
                assert len(data['processing_data']['screenshot']) > 100, "El screenshot (base64) está vacío"

                print("\n✅ PRUEBA SERVIDOR A (INTEGRACIÓN): EXITOSA.")
                print("   Respuesta 'status: success' y JSON consolidado recibido.")

    except asyncio.TimeoutError:
        print(f"\n❌ ERROR: Timeout. El servidor A ({SERVER_URL}) tardó demasiado.")
        print("   Asegúrate de que AMBOS servidores (A y B) estén corriendo.")
        sys.exit(1)
    except aiohttp.ClientConnectorError:
        print(f"\n❌ ERROR: No se pudo conectar al Servidor A ({SERVER_URL}).")
        print("   Asegúrate de que 'server_scraping.py' esté corriendo en la Terminal 2.")
        sys.exit(1)
    except AssertionError as e:
        print(f"\n❌ FALLÓ LA PRUEBA (Assert): {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_scraper())