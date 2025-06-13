import multiprocessing
import os
from datetime import datetime

# Función que cada proceso ejecuta
def escribir_log(lock, archivo):
    with lock:  # Entra en sección crítica
        with open(archivo, "a") as f:
            pid = os.getpid()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"Proceso PID {pid} escribió en {timestamp}\n")

def main():
    archivo_log = "log.txt"
    lock = multiprocessing.Lock()  # Crear un candado
    procesos = []

    # Crear 4 procesos
    for _ in range(4):
        p = multiprocessing.Process(target=escribir_log, args=(lock, archivo_log))
        procesos.append(p)
        p.start()

    # Esperar a que todos terminen
    for p in procesos:
        p.join()

    print("Todos los procesos terminaron. Ver 'log.txt'.")

if __name__ == "__main__":
    main()
