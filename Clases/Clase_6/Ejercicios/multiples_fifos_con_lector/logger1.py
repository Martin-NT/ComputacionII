import time

with open('/tmp/fifo_logger1', 'w') as fifo:
    for i in range(5):
        fifo.write(f'[LOGGER 1] Mensaje {i}\n')
        fifo.flush()
        time.sleep(1)
