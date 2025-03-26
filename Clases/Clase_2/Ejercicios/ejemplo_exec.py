import os

pid = os.fork()

if pid == 0:  # Código del proceso hijo
    print("Proceso hijo antes de exec")
    os.execvp("ls", ["ls", "-l"])  # Ejecuta `ls -l`
    
else:  # Código del proceso padre
    print(f"Soy el proceso padre, mi hijo tiene PID {pid}")

#🔍 ¿Qué esperar?
#   El proceso hijo imprimirá la lista de archivos con detalles.
#   El padre solo mostrará un mensaje con el PID del hijo.