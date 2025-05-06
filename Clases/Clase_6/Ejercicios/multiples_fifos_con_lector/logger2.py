import time

with open('/tmp/fifo_logger2', 'w') as fifo:
    for i in range(5):
        fifo.write(f'[LOGGER 2] Mensaje {i}\n')
        fifo.flush()
        time.sleep(2)
