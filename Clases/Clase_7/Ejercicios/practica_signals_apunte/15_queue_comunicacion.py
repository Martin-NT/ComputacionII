import signal
import threading
import time
import os
from queue import Queue, Empty

# Cola de comandos
comandos = Queue()

def worker(nombre):
    while True:
        try:
            cmd = comandos.get(timeout=1)
            if cmd == 'stop':
                print(f"🛑 Hilo {nombre} detenido por orden.")
                break
        except Empty:
            print(f"🔧 Hilo {nombre} trabajando...")
            time.sleep(0.5)

def handler(signum, frame):
    print("📣 Señal SIGINT recibida. Enviando 'stop' a todos los hilos...")
    for _ in range(3):
        comandos.put('stop')

if __name__ == '__main__':
    print(f"PID: {os.getpid()}")
    signal.signal(signal.SIGINT, handler)

    hilos = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(f"H{i+1}",))
        t.start()
        hilos.append(t)

    for t in hilos:
        t.join()

    print("✅ Todos los hilos terminaron.")
