from multiprocessing import Process, Value, Lock

def inc(v, n, lock):
    for _ in range(n):
        with lock:
            v.value += 1

if __name__ == '__main__':
    N = 50_000
    contador = Value('i', 0)
    lock = Lock()
    p1 = Process(target=inc, args=(contador, N, lock))
    p2 = Process(target=inc, args=(contador, N, lock))
    p1.start(); p2.start(); p1.join(); p2.join()
    print('Resultado seguro:', contador.value)