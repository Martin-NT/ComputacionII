from multiprocessing import Process, Value, Lock
import time

# Proceso que actualiza el valor compartido con el tiempo actual
def actualizador(tiempo, lock):
    while True:
        with lock:
            tiempo.value = time.time()
        time.sleep(1)

# Proceso que lee el valor compartido y detecta incoherencias temporales
def verificador(tiempo, lock):
    previo = time.time()
    while True:
        with lock:
            actual = tiempo.value
        delta = actual - previo
        if delta > 1.0:
            print(f"⚠️ Incoherencia detectada: salto de {delta:.2f} segundos")
        previo = actual
        time.sleep(0.5)

if __name__ == "__main__":
    tiempo = Value('d', time.time())  # valor compartido tipo double
    lock = Lock()  # sincronización

    # Crear 3 procesos actualizadores
    actualizadores = [Process(target=actualizador, args=(tiempo, lock)) for _ in range(3)]
    # Crear 1 proceso verificador
    lector = Process(target=verificador, args=(tiempo, lock))

    for p in actualizadores:
        p.start()
    lector.start()

    for p in actualizadores:
        p.join()
    lector.join()
