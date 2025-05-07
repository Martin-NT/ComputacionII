import os
import signal
import time

def handler(signum, frame):
    print(f"📨 Señal recibida: {signum}")

# Registrar handler
signal.signal(signal.SIGUSR1, handler)

pid = os.getpid()
print(f"🆔 Mi PID es: {pid}")
print("⌛ Esperando señal SIGUSR1...")

# Esperamos una señal externa
while True:
    time.sleep(1)
