import os

# Creamos dos FIFOs para comunicación bidireccional
for fifo in ['/tmp/chat_a_b', '/tmp/chat_b_a']:
    try:
        os.mkfifo(fifo)
        print(f'FIFO creado: {fifo}')
    except FileExistsError:
        print(f'Ya existe: {fifo}')
