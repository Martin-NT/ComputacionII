import os

def main():
    # Crear el pipe: devuelve dos descriptores de archivo (enteros)
    lector, escritor = os.pipe()

    pid = os.fork()

    if pid == 0:
        # Proceso hijo
        os.close(lector)  # Cierra el extremo de lectura (no lo necesita)

        mensaje = "Hola desde el hijo!".encode('utf-8')  # Codificamos el string como bytes
        os.write(escritor, mensaje)  # Escribimos al pipe
        os.close(escritor)  # Cerramos el extremo de escritura

    else:
        # Proceso padre
        os.close(escritor)  # Cierra el extremo de escritura (no lo necesita)

        # Lee hasta 1024 bytes del pipe
        mensaje_recibido = os.read(lector, 1024)
        print("Mensaje recibido del hijo:", mensaje_recibido.decode('utf-8'))  # Decodificamos los bytes

        os.close(lector)  # Cerramos el extremo de lectura
        os.wait()  # Esperamos al hijo

if __name__ == "__main__":
    main()
