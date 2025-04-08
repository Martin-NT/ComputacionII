import os
import multiprocessing

# Función que se ejecutará en el proceso hijo
def child_process(w):
    os.close(r)  # Cerrar el extremo de lectura en el hijo (no lo usa)
    
    mensaje = b"Hola desde el hijo!\n"  # Mensaje en formato bytes
    os.write(w, mensaje)  # Escribir mensaje en el pipe

    os.close(w)  # Cerrar el extremo de escritura después de usarlo

if __name__ == "__main__":
    # Crear el pipe: devuelve dos file descriptors (lectura y escritura)
    r, w = os.pipe()

    # Crear un proceso hijo y pasarle el descriptor de escritura
    p = multiprocessing.Process(target=child_process, args=(w,))
    p.start()

    os.close(w)  # Cerrar el extremo de escritura en el padre (no lo usa)

    # Leer hasta 1024 bytes del pipe
    mensaje = os.read(r, 1024)
    print("Padre recibió:", mensaje.decode())  # Decodificar a string y mostrar

    os.close(r)  # Cerrar el extremo de lectura después de usarlo

    p.join()  # Esperar a que el hijo termine
