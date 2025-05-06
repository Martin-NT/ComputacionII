import os

fifos = ['/tmp/fifo1', '/tmp/fifo2']

for fifo in fifos:
    try:
        os.mkfifo(fifo)
        print(f'FIFO creado: {fifo}')
    except FileExistsError:
        print(f'Ya existe: {fifo}')
