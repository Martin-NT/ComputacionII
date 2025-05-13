import math
from multiprocessing import Process, Lock

# Función que calcula los números primos en un rango
def calcular_primos(rango_inicio, rango_fin, lock):
    primos = []
    for num in range(rango_inicio, rango_fin):
        if es_primo(num):
            primos.append(num)
    # Sincronizar el acceso al archivo primos.txt usando Lock
    with lock:
        with open("primos.txt", "a") as archivo:
            for primo in primos:
                archivo.write(f"{primo}\n")

# Función que verifica si un número es primo
def es_primo(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

if __name__ == "__main__":
    N = 8  # Número de procesos
    rango_max = 100000  # Máximo valor para calcular primos
    rango_por_proceso = rango_max // N

    lock = Lock()  # Sincronización para el acceso al archivo
    procesos = []

    # Crear procesos para calcular primos en rangos disjuntos
    for i in range(N):
        rango_inicio = i * rango_por_proceso
        rango_fin = (i + 1) * rango_por_proceso
        if i == N - 1:  # Último proceso, hasta el máximo valor
            rango_fin = rango_max
        proceso = Process(target=calcular_primos, args=(rango_inicio, rango_fin, lock))
        procesos.append(proceso)

    # Iniciar los procesos
    for proceso in procesos:
        proceso.start()

    # Esperar a que todos los procesos terminen
    for proceso in procesos:
        proceso.join()

    print(f"Cálculo de primos completado. Los resultados se guardaron en 'primos.txt'.")
