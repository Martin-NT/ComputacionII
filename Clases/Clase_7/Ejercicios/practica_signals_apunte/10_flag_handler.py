import os
import signal
import time

# Variable global que el handler va a modificar
interrumpido = False

def handler(signum, frame):
    global interrumpido
    interrumpido = True  # ✅ Solo se cambia el estado, sin efectos colaterales

def proceso():
    signal.signal(signal.SIGUSR1, handler)
    print(f"🔧 PID del proceso: {os.getpid()}")
    print("⌛ Esperando señal SIGUSR1...")

    while not interrumpido:
        print("💼 Trabajando...")
        time.sleep(1)

    print("🛑 Señal recibida. Terminando el proceso de forma segura.")

if __name__ == '__main__':
    proceso()
