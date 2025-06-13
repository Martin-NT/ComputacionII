import multiprocessing
import os

def escribir(lock):
    with lock:
        with open("salida.txt", "a") as f:
            for i in range(5):
                f.write(f"[PID {os.getpid()}] Línea {i}\n")

if __name__ == "__main__":
    lock = multiprocessing.Lock()
    procesos = []

    for _ in range(5):
        p = multiprocessing.Process(target=escribir, args=(lock,))
        p.start()
        procesos.append(p)

    for p in procesos:
        p.join()
