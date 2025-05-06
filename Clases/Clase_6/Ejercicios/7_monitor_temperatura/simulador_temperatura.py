import random
import time
fifo_path = '/tmp/temp_fifo'

with open(fifo_path, 'w') as fifo:
    while True:
        temp = random.randint(20, 30)
        fifo.write(f"{temp}\n")
        time.sleep(1)
