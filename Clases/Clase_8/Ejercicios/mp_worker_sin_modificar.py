import time

def tarea(nombre):
    print(f"[{nombre}] Iniciando tarea...")
    time.sleep(2)
    print(f"[{nombre}] Tarea finalizada.")

if __name__ == '__main__':
    inicio = time.time()

    tarea("Proceso 1")
    tarea("Proceso 2")

    fin = time.time()
    print(f"Tiempo total: {fin - inicio:.2f} segundos")
