import os
import signal
import time

detener = False

def handler(signum, frame):
    global detener
    detener = True  # ✅ Solo se cambia la variable

def ciclo():
    signal.signal(signal.SIGUSR1, handler)
    print(f"🧪 Esperando SIGUSR1 para terminar. PID: {os.getpid()}")
    
    while not detener:
        print("⏳ Procesando...")
        time.sleep(1)

    print("✅ Señal recibida. Finalización correcta.")

if __name__ == '__main__':
    ciclo()
