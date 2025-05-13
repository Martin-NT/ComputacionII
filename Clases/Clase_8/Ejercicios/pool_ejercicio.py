from multiprocessing import Pool

def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

if __name__ == '__main__':
    numeros = [5, 6, 7, 8]
    with Pool(processes=4) as pool:
        resultados = pool.map(factorial, numeros)
    print(f"Factoriales: {resultados}")
