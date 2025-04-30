from multiprocessing import Process, Queue, current_process
import time
import random

# Función para cada productor
def productor(q, id):
    for i in range(3):
        valor = f"Mensaje {i} de Productor {id}"
        print(f"[{current_process().name}] Enviando: {valor}")
        q.put(valor)
        time.sleep(random.uniform(0.5, 1.5))

# Consumidor que procesa todos los mensajes
def consumidor(q, total_mensajes):
    for _ in range(total_mensajes):
        mensaje = q.get()
        print(f"[{current_process().name}] Recibido: {mensaje}")

if __name__ == "__main__":
    queue = Queue()
    
    # Crear múltiples productores
    productores = []
    num_productores = 3
    for i in range(num_productores):
        p = Process(target=productor, args=(queue, i), name=f"Productor-{i}")
        productores.append(p)

    # Calcular cuántos mensajes totales se esperan
    total_mensajes = num_productores * 3

    # Consumidor
    consumidor_proceso = Process(target=consumidor, args=(queue, total_mensajes), name="Consumidor")

    # Iniciar procesos
    for p in productores:
        p.start()
    consumidor_proceso.start()

    # Esperar a que todos terminen
    for p in productores:
        p.join()
    consumidor_proceso.join()

    print("[Main] Todos los procesos han terminado.")
