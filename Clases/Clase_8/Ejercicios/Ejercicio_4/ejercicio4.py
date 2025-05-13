from multiprocessing import Process
from threading import Thread
import time

# Función recursiva de Fibonacci (no optimizada)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Función para ejecutar 4 tareas de fibonacci(n) y medir tiempo
def run_benchmark(worker, label):
    n = 35
    start = time.perf_counter()
    tasks = [worker(target=fibonacci, args=(n,)) for _ in range(4)]
    for t in tasks:
        t.start()
    for t in tasks:
        t.join()
    end = time.perf_counter()
    duration = end - start
    print(f"{label} took {duration:.2f} seconds")

# Ejecutar benchmark con hilos y procesos
if __name__ == "__main__":
    run_benchmark(Thread, "Threading")
    run_benchmark(Process, "Multiprocessing")
