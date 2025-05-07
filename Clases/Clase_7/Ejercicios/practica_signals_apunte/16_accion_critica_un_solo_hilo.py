import signal
import threading
import time
import os

# Evento para activar emergencia
emergencia = threading.Event()

def trabajador(nombre):
    while not emergencia.is_set():
        print(f"🛠️ Hilo {nombre} operativo...")
        time.sleep(1)
    print(f"⚠️ Hilo {nombre} detectó señal de emergencia.")

def seguridad():
    print("🔒 Hilo de seguridad esperando emergencia...")
    emergencia.wait()
    print("🚨 ¡Apagado de emergencia activado!")

def handler(signum, frame):
    print("📣 Señal SIGINT recibida. Activando protocolo de seguridad...")
    emergencia.set()

if __name__ == '__main__':
    print(f"PID: {os.getpid()}")
    signal.signal(signal.SIGINT, handler)

    h1 = threading.Thread(target=trabajador, args=("Motor",))
    h2 = threading.Thread(target=trabajador, args=("Bomba",))
    h3 = threading.Thread(target=seguridad)

    h1.start()
    h2.start()
    h3.start()

    h1.join()
    h2.join()
    h3.join()

    print("✅ Todos los subsistemas detenidos.")
