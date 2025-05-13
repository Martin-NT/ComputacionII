import time
import random
from multiprocessing import Process, Pipe, Queue, Manager
import matplotlib.pyplot as plt

# Método usando Pipe
def ipc_pipe(pipe, num_elements):
    for i in range(num_elements):
        pipe.send(random.randint(1, 100))
    pipe.send(None)  # Señal para terminar
    pipe.close()

# Método usando Queue
def ipc_queue(queue, num_elements):
    for i in range(num_elements):
        queue.put(random.randint(1, 100))
    queue.put(None)  # Señal para terminar

# Método usando Manager().list
def ipc_manager_list(manager_list, num_elements):
    for i in range(num_elements):
        manager_list.append(random.randint(1, 100))

def benchmark_ipc(method, num_elements):
    start_time = time.perf_counter()

    if method == "pipe":
        parent_conn, child_conn = Pipe()
        p = Process(target=ipc_pipe, args=(child_conn, num_elements))
        p.start()
        # Leer los datos enviados por el proceso
        while True:
            data = parent_conn.recv()
            if data is None:
                break
        p.join()

    elif method == "queue":
        queue = Queue()
        p = Process(target=ipc_queue, args=(queue, num_elements))
        p.start()
        # Leer los datos de la cola
        while True:
            data = queue.get()
            if data is None:
                break
        p.join()

    elif method == "manager_list":
        with Manager() as manager:
            manager_list = manager.list()
            p = Process(target=ipc_manager_list, args=(manager_list, num_elements))
            p.start()
            p.join()

    end_time = time.perf_counter()
    return end_time - start_time

def run_benchmark():
    num_elements = 10**6  # 1 millón de elementos
    methods = ["pipe", "queue", "manager_list"]
    times = []

    for method in methods:
        print(f"Ejecutando benchmark con {method}...")
        elapsed_time = benchmark_ipc(method, num_elements)
        times.append(elapsed_time)
        print(f"Tiempo con {method}: {elapsed_time:.4f} segundos")

    return methods, times

if __name__ == "__main__":
    methods, times = run_benchmark()

    # Graficar los resultados
    plt.bar(methods, times, color=['blue', 'green', 'red'])
    plt.title('Comparación de métodos IPC')
    plt.xlabel('Método IPC')
    plt.ylabel('Tiempo (segundos)')
    plt.show()
