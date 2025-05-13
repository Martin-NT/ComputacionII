import time
import requests
from multiprocessing import Process, Queue

# Función que simula la descarga de una URL
def descargar_url(url, queue):
    start = time.time()
    # Simular descarga (realmente, hacemos un request)
    response = requests.get(url)
    end = time.time()
    duration = end - start
    # Registramos el resultado en la cola con el PID y duración
    queue.put((url, response.status_code, duration))

# Función del proceso maestro que reparte las tareas
def maestro(urls, k, queue):
    # Crear k procesos worker para repartir las URLs
    workers = [Process(target=descargar_url, args=(url, queue)) for url in urls]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()

    # Generar el reporte ordenado por tiempo de descarga
    resultados = []
    while not queue.empty():
        resultados.append(queue.get())

    # Ordenar por duración y mostrar el reporte
    resultados.sort(key=lambda x: x[2])  # Ordenamos por el tiempo de descarga
    print("Reporte de descargas:")
    for url, status, duration in resultados:
        print(f"{url} - Estado: {status}, Duración: {duration:.2f}s")

if __name__ == "__main__":
    # Lista de URLs para descargar (simulada con ejemplo)
    urls = ["https://httpbin.org/delay/1", "https://httpbin.org/delay/2", "https://httpbin.org/delay/3"]
    queue = Queue()  # Cola para almacenar los resultados
    k = 3  # Número de workers (procesos)

    # Llamar al proceso maestro
    maestro(urls, k, queue)
