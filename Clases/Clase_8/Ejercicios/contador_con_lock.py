from multiprocessing import Process, Value, Lock
import time

def incrementar(contador, lock):
    for _ in range(100000):
        with lock:
            contador.value += 1

if __name__ == '__main__':
    contador = Value('i', 0)
    lock = Lock()

    p1 = Process(target=incrementar, args=(contador, lock))
    p2 = Process(target=incrementar, args=(contador, lock))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print(f"Contador final: {contador.value}")
