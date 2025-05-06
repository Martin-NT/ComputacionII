import os
import select

fifos = ['/tmp/fifo1', '/tmp/fifo2']
fds = [os.open(f, os.O_RDONLY | os.O_NONBLOCK) for f in fifos]

print("Lector listo. Esperando mensajes...")

try:
    while True:
        rlist, _, _ = select.select(fds, [], [])
        for fd in rlist:
            data = os.read(fd, 1024)
            if data:
                print(f"[FIFO {fd}] Recibido:", data.decode().strip())
            else:
                print(f"[FIFO {fd}] Cerrado por el escritor")
except KeyboardInterrupt:
    print("Saliendo...")
finally:
    for fd in fds:
        os.close(fd)
