import select

fifo_paths = ['/tmp/fifo_logger1', '/tmp/fifo_logger2']
fifo_files = [open(path, 'r') for path in fifo_paths]

while True:
    readable, _, _ = select.select(fifo_files, [], [])
    for fifo in readable:
        line = fifo.readline()
        if line:
            print(f'[LECTOR] Recibido: {line.strip()}')
