from multiprocessing import Pool
import time

def saludar(nombre):
    time.sleep(1)
    print(f"Hola {nombre}!")

if __name__ == '__main__':
    nombres = ['Ana', 'Luis', 'Carlos']
    with Pool(processes=3) as pool:
        for nombre in nombres:
            pool.apply_async(saludar, args=(nombre,))
        pool.close()
        pool.join()
