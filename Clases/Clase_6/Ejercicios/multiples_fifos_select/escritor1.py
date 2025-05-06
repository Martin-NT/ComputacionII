import os
import time

with open('/tmp/fifo1', 'w') as fifo:
    for i in range(5):
        mensaje = f"[escritor1] mensaje {i}\n"
        fifo.write(mensaje)
        fifo.flush()
        time.sleep(1)
