# Prueba de integración para el Servidor B (Processing)
import socket
import sys
import os

# --- INICIO: Hack para importar módulos del directorio padre ---
# Necesario para que el test pueda encontrar la carpeta 'common'
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    from common.protocol import send_message, recv_message
except ImportError:
    print("\nError: No se pudo importar 'common.protocol'.")
    print("Asegúrate de que 'common/protocol.py' exista en el directorio raíz del TP.")
    sys.exit(1)


HOST = "127.0.0.1"
PORT = 9090 # El puerto del Servidor B

def test_processor():
    """
    Prueba una conexión directa al Servidor B (server_processing.py)
    """
    print("Iniciando prueba del Servidor B (Processing)...")
    try:
        with socket.create_connection((HOST, PORT), timeout=15) as sock:
            
            # 1. Enviar la tarea al Servidor B
            print(f"Enviando tarea a {HOST}:{PORT}...")
            send_message(sock, {"task": "analyze", "url": "https://example.com"})
            
            # 2. Recibir la respuesta
            resp = recv_message(sock)

            # 3. Verificar la respuesta
            assert 'status' in resp, "Respuesta JSON no tiene 'status'"
            assert resp['status'] == 'ok', "El status de la operación no fue 'ok'"
            assert 'processing_data' in resp, "Respuesta JSON no tiene 'processing_data'"
            
            data = resp['processing_data']
            assert 'screenshot' in data, "processing_data no tiene 'screenshot'"
            assert 'performance' in data, "processing_data no tiene 'performance'"
            assert 'thumbnails' in data, "processing_data no tiene 'thumbnails'"
            
            print("\n✅ PRUEBA SERVIDOR B: EXITOSA.")
            print("   Respuesta 'status: ok' recibida.")
            print(f"   Datos recibidos: {list(data.keys())}")

    except socket.timeout:
        print(f"\n❌ ERROR: Timeout. El servidor B ({HOST}:{PORT}) tardó demasiado.")
        sys.exit(1)
    except ConnectionRefusedError:
        print(f"\n❌ ERROR: No se pudo conectar al Servidor B ({HOST}:{PORT}).")
        print("   Asegúrate de que 'server_processing.py' esté corriendo en la Terminal 1.")
        sys.exit(1)
    except AssertionError as e:
        print(f"\n❌ FALLÓ LA PRUEBA (Assert): {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_processor()