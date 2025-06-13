import multiprocessing
import os
import time
import random

# Función que simula trabajo en una zona crítica
def usar_puesto(semaforo):
    pid = os.getpid()
    
    print(f"Proceso {pid} esperando un puesto...")
    with semaforo:  # entra si hay lugar (semaforo > 0)
        print(f"--> Proceso {pid} ENTRÓ al puesto.")
        time.sleep(random.uniform(1, 3))  # simula trabajo
        print(f"                                        <-- Proceso {pid} SALIÓ del puesto.")

def main():
    # Solo 3 puestos disponibles al mismo tiempo
    semaforo = multiprocessing.Semaphore(3)
    procesos = []

    # Crear 10 procesos
    for _ in range(10):
        p = multiprocessing.Process(target=usar_puesto, args=(semaforo,))
        procesos.append(p)
        p.start()

    # Esperar a que todos terminen
    for p in procesos:
        p.join()

    print("Todos los procesos han terminado.")

if __name__ == "__main__":
    main()
