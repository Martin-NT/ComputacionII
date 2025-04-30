from multiprocessing import Process, Queue
import random
import time

# Función de productor, genera un número aleatorio y lo manda a la cola
def productor(q, id):
    for _ in range(5):  # Cada productor genera 5 números aleatorios
        num = random.randint(1, 100)
        print(f"Productor {id}: enviando {num}")
        q.put(num)  # Enviar el número a la cola
        time.sleep(random.uniform(0.1, 1.0))

# Función de consumidor, recibe números de la cola y los suma
def consumidor(q, num_productores):
    total = 0
    for _ in range(num_productores * 5):  # El consumidor recibe 5 números de cada productor
        num = q.get()
        total += num
        print(f"Consumidor: recibido {num}. Suma actual: {total}")
    print(f"Consumidor: Total final: {total}")

if __name__ == "__main__":
    queue = Queue()
    num_productores = 3  # Número de productores

    # Crear procesos productores
    productores = [Process(target=productor, args=(queue, i)) for i in range(num_productores)]

    # Crear proceso consumidor
    c = Process(target=consumidor, args=(queue, num_productores))

    # Iniciar procesos
    for p in productores:
        p.start()
    c.start()

    # Esperar a que los procesos terminen
    for p in productores:
        p.join()
    c.join()

    print("[Main] Todos los procesos han finalizado.")
