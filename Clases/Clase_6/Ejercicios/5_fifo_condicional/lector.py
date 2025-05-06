import os
import time

fifo_path = '/tmp/fifo_condicional'
max_retries = 5
retries = 0

while retries < max_retries:
    try:
        fd = os.open(fifo_path, os.O_RDONLY | os.O_NONBLOCK)
        with os.fdopen(fd, 'r') as fifo:
            data = fifo.read()
            print(f"Recibido: {data}")
        break
    except OSError:
        print("FIFO no disponible, reintentando...")
        retries += 1
        time.sleep(1)

if retries == max_retries:
    print("No se pudo abrir el FIFO después de varios intentos.")
