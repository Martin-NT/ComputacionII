import signal
import threading
import time
import os

# Evento compartido
detener = threading.Event()

def worker(nombre):
    while not detener.is_set():
        print(f"🔧 Hilo {nombre} trabajando...")
        time.sleep(1)
    print(f"🛑 Hilo {nombre} finalizó.")

def handler(signum, frame):
    print("📣 Señal SIGINT recibida.")
    detener.set()

if __name__ == '__main__':
    print(f"PID del proceso: {os.getpid()}")
    signal.signal(signal.SIGINT, handler)

    hilos = []
    for i in range(3):  # tres hilos
        t = threading.Thread(target=worker, args=(f"H{i+1}",))
        t.start()
        hilos.append(t)

    for t in hilos:
        t.join()

    print("✅ Todos los hilos terminaron.")
