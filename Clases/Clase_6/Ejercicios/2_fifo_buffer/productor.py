import os
import time

fifo_path = '/tmp/test_fifo'
with open(fifo_path, 'w') as fifo:
    for i in range(1, 101):
        fifo.write(f"{i}\n")
        time.sleep(0.1)
