import multiprocessing
import os

def escribir():
    with open("salida.txt", "a") as f:
        for i in range(5):
            f.write(f"[PID {os.getpid()}] Línea {i}\n")

if __name__ == "__main__":
    procesos = []

    for _ in range(5):  # lanzamos 5 procesos
        p = multiprocessing.Process(target=escribir)
        p.start()
        procesos.append(p)

    for p in procesos:
        p.join()
