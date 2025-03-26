import os
import time

pid = os.fork()

if pid == 0:  # Código del hijo
    print("Soy el proceso hijo, voy a dormir 3 segundos...")
    time.sleep(3)
    print("Hijo terminando.")
    
else:  # Código del padre
    print("Soy el proceso padre, esperando a mi hijo...")
    pid_hijo, status = os.wait()  # Bloquea hasta que el hijo termine
    print(f"El proceso hijo {pid_hijo} terminó con estado {status}")

#🔍 ¿Qué esperar?
#   El hijo dormirá 3 segundos antes de terminar.
#   El padre esperará y no imprimirá su mensaje final hasta que el hijo termine.