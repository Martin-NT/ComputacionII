import signal
import time
import multiprocessing
import os
import sys

def proceso_hijo():
    print(f"👶 Hijo iniciado (PID={os.getpid()})")
    while True:
        time.sleep(1)
        print("🧒 Hijo trabajando...")

def handler_padre(signum, frame):
    print("🛑 Padre recibió SIGINT. Terminando al hijo...")
    hijo.terminate()
    hijo.join()
    print("✅ Hijo terminado. Cerrando programa.")
    sys.exit(0)

# Crear el proceso hijo
hijo = multiprocessing.Process(target=proceso_hijo)
hijo.start()

# Registrar handler en el padre
signal.signal(signal.SIGINT, handler_padre)

print(f"👨 Padre ejecutándose (PID={os.getpid()})")
while True:
    time.sleep(1)