from multiprocessing import Process, Queue, current_process
import time
import random

def productor(q, num_tareas):
    for i in range(num_tareas):
        tarea = f"Tarea-{i}"
        print(f"[{current_process().name}] Enviando: {tarea}")
        q.put(tarea)
    # Enviar una señal de parada a cada consumidor
    for _ in range(3):
        q.put("FIN")

def consumidor(q):
    while True:
        tarea = q.get()
        if tarea == "FIN":
            print(f"[{current_process().name}] Terminando.")
            break
        print(f"[{current_process().name}] Procesando: {tarea}")
        time.sleep(random.uniform(0.5, 1.5))

if __name__ == "__main__":
    queue = Queue()
    num_consumidores = 3

    p_productor = Process(target=productor, args=(queue, 9), name="Productor")
    consumidores = [Process(target=consumidor, args=(queue,), name=f"Consumidor-{i}") for i in range(num_consumidores)]

    p_productor.start()
    for c in consumidores:
        c.start()

    p_productor.join()
    for c in consumidores:
        c.join()

    print("[Main] Todos los procesos finalizaron.")
