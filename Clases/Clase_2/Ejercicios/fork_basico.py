import os

pid = os.fork()  # Crea un proceso hijo

if pid == 0:
    print("Soy el proceso hijo")
else:
    print(f"Soy el proceso padre, mi hijo tiene PID {pid}")

#🔍 ¿Qué esperar?
#   Se imprimirán dos mensajes, uno desde el padre y otro desde el hijo.
#   Notarás que ambos procesos continúan ejecutando el código desde fork() pero con caminos distintos.