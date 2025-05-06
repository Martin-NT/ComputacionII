import os
fd = os.open('/tmp/mi_fifo', os.O_RDONLY)
data = os.read(fd, 1024)
print('Mensaje recibido:', data.decode())
os.close(fd)


#✅ Paso 3: Ejecutar

# Primero, en una terminal ejecutá: python3 leer_fifo.py
# Luego, en otra terminal: python3 escribir_fifo.py

# Si invertís el orden, notarás que el lector se queda esperando. ¡Esto es importante!