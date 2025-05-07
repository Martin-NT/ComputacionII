import signal
import time

def handler(signum, frame):
    if signum == signal.SIGINT:
        print("⚠️ Recibí SIGINT (Ctrl+C)")
    elif signum == signal.SIGTERM:
        print("🚨 Recibí SIGTERM (terminación)")
    else:
        print(f"❓ Señal desconocida: {signum}")

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)

print("⏳ Esperando señales...")

while True:
    time.sleep(1)
