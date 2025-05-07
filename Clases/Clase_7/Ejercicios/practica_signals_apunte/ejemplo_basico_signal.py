import signal
import time

# Paso 2: Definimos el manejador
def mi_handler(signum, frame):
    print(f"⚠️ Señal recibida: {signum}. Ignorando Ctrl+C...")

# Paso 3: Asociamos SIGINT con el manejador
signal.signal(signal.SIGINT, mi_handler)

print("⏳ El programa está corriendo. Presioná Ctrl+C para probar...")

# Paso 4: Bucle infinito
while True:
    time.sleep(1)  # Simula que el proceso sigue haciendo algo
