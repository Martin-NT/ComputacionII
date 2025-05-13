from multiprocessing import Pool

def cuadrado(n):
    return n * n

if __name__ == '__main__':
    numeros = [1, 2, 3, 4, 5]
    with Pool(processes=2) as pool:
        resultados = pool.map(cuadrado, numeros)
    print(f"Resultados: {resultados}")
