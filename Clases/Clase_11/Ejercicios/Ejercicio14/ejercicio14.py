import time
import os
import signal

def handler(signum, frame):
    print(f"Proceso {os.getpid()} recibió señal {signum}, terminando...")
    exit(0)

signal.signal(signal.SIGTERM, handler)

print(f"Proceso Python {os.getpid()} durmiendo 10 segundos...")
time.sleep(10)
print("Proceso finalizó normalmente.")
