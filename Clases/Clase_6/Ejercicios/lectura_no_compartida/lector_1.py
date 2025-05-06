# lector_1.py
import os

fd = os.open('/tmp/fifo_cursor', os.O_RDONLY)
print('Lector 1 lee:', os.read(fd, 3).decode())  # Leerá 'ABC'
os.close(fd)
