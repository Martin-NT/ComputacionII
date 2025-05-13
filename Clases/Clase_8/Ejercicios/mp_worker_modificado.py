import time
from multiprocessing import Process

def tarea(nombre):
    print(f"[{nombre}] Iniciando tarea...")
    time.sleep(2)
    print(f"[{nombre}] Tarea finalizada.")

if __name__ == '__main__':
    inicio = time.time()

    p1 = Process(target=tarea, args=("Proceso 1",))
    p2 = Process(target=tarea, args=("Proceso 2",))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    fin = time.time()
    print(f"Tiempo total: {fin - inicio:.2f} segundos")
