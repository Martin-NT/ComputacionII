from multiprocessing import Process
import os
import time

def tarea(nombre):
    print(f"[{nombre}] Inicia en PID: {os.getpid()}")
    time.sleep(2)
    print(f"[{nombre}] Finaliza")

if __name__ == '__main__':
    print(f"[Padre] PID: {os.getpid()}")

    p1 = Process(target=tarea, args=('Proceso 1',))
    p2 = Process(target=tarea, args=('Proceso 2',))

    p1.start()
    p2.start()

    print(f"[Padre] Proceso 1 activo: {p1.is_alive()}")
    print(f"[Padre] Proceso 2 activo: {p2.is_alive()}")

    p1.join()
    p2.join()

    print(f"[Padre] Ambos procesos han finalizado.")
