# escribir_fifo_cursor.py
import os

fd = os.open('/tmp/fifo_cursor', os.O_WRONLY)
os.write(fd, b'ABCDEF')
os.close(fd)
