import os
import time

with open('/tmp/fifo2', 'w') as fifo:
    for i in range(5):
        mensaje = f"[escritor2] mensaje {i}\n"
        fifo.write(mensaje)
        fifo.flush()
        time.sleep(1.5)

