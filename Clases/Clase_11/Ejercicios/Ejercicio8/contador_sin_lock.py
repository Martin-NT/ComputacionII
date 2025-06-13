import multiprocessing

def incrementar(contador):
    for _ in range(100000):
        contador.value += 1  # acceso sin protección

def main():
    contador = multiprocessing.Value('i', 0)  # entero compartido sin Lock
    p1 = multiprocessing.Process(target=incrementar, args=(contador,))
    p2 = multiprocessing.Process(target=incrementar, args=(contador,))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print("Valor final sin Lock:", contador.value)

if __name__ == "__main__":
    main()
