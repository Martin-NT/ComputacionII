import multiprocessing

def incrementar(contador, lock):
    for _ in range(100000):
        with lock:  # sección crítica protegida
            contador.value += 1

def main():
    contador = multiprocessing.Value('i', 0)  # entero compartido
    lock = multiprocessing.Lock()

    p1 = multiprocessing.Process(target=incrementar, args=(contador, lock))
    p2 = multiprocessing.Process(target=incrementar, args=(contador, lock))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print("Valor final con Lock:", contador.value)

if __name__ == "__main__":
    main()
