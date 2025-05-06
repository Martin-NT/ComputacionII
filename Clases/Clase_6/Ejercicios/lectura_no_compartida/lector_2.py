# lector_2.py
import os

fd = os.open('/tmp/fifo_cursor', os.O_RDONLY)
print('Lector 2 lee:', os.read(fd, 3).decode())  # Leerá 'DEF' o nada
os.close(fd)