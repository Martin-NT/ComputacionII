import signal
import threading
import time
import os

# Bandera compartida
terminar = threading.Event()

def worker(nombre):
    while not terminar.is_set():
        print(f"🔧 Hilo {nombre} trabajando...")
        time.sleep(1)
    print(f"🛑 Hilo {nombre} finalizó con orden.")

def signal_handler(signum, frame):
    print("📣 Señal recibida en hilo principal")
    terminar.set()

if __name__ == '__main__':
    print(f"🚦 PID del proceso: {os.getpid()}")
    signal.signal(signal.SIGINT, signal_handler)  # Solo en el hilo principal

    hilos = []
    for i in range(2):
        t = threading.Thread(target=worker, args=(f"H{i+1}",)).start()
        hilos.append(t)

    # Espera a que terminen
    for h in hilos:
        h.join()

    print("✅ Todos los hilos terminaron.")
