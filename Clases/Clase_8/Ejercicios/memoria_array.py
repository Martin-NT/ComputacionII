from multiprocessing import Process, Array

def multiplicar(arr):
    for i in range(len(arr)):
        arr[i] *= 2

if __name__ == '__main__':
    datos = Array('i', [1, 2, 3, 4, 5])

    p = Process(target=multiplicar, args=(datos,))
    p.start()
    p.join()

    print(f"Array modificado: {list(datos)}")
