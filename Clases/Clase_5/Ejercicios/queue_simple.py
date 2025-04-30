from multiprocessing import Process, Queue
import time

# Función del productor
def productor(q):
    for i in range(5):
        print(f"[Productor] Enviando: {i}")
        q.put(i)  # Enviar a la Queue
        time.sleep(1)

# Función del consumidor
def consumidor(q):
    for _ in range(5):
        valor = q.get()  # Recibir de la Queue
        print(f"[Consumidor] Recibido: {valor}")

if __name__ == "__main__":
    queue = Queue()  # Crear la Queue compartida

    # Crear procesos
    p1 = Process(target=productor, args=(queue,))
    p2 = Process(target=consumidor, args=(queue,))

    # Iniciar procesos
    p1.start()
    p2.start()

    # Esperar que terminen
    p1.join()
    p2.join()

    print("[Main] Procesos finalizados.")
