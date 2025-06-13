import os
import time

def hijo(read_fd):
    os.close(write_fd)  # El hijo solo lee
    mensaje = os.read(read_fd, 1024)
    print(f"[Hijo] Recibido: {mensaje.decode()}")
    os.close(read_fd)

def padre(write_fd):
    os.close(read_fd)  # El padre solo escribe
    os.write(write_fd, b"Hola desde el padre!")
    time.sleep(10)  # Esperamos un rato para ver los descriptores con lsof
    os.close(write_fd)

if __name__ == "__main__":
    read_fd, write_fd = os.pipe()
    pid = os.fork()

    if pid == 0:
        hijo(read_fd)
    else:
        padre(write_fd)
