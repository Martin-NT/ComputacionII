import os

fifo_path = '/tmp/test_fifo'

# Abrimos el FIFO para leer los datos
with open(fifo_path, 'r') as fifo:
    last_number = None
    while True:
        data = fifo.readline()
        if data:  # Si hay datos en FIFO
            number = int(data.strip())
            if last_number is not None and number != last_number + 1:
                print(f"Error: Se saltó el número {last_number + 1}")
            last_number = number
            print(f"Recibido: {number}")
