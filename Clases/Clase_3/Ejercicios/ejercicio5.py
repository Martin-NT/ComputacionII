"""Ejercicio 5: Proceso zombi temporal"""
# Crea un programa que genere un proceso hijo que termine inmediatamente, pero el padre no debe recoger 
# su estado de salida durante algunos segundos. Observa su estado como zombi con herramientas del sistema.

import os
import time

pid = os.fork()

if pid == 0:  # Código del proceso hijo
    print(f"- [Proceso Hijo] PID: {os.getpid()} --> Finalizando inmediatamente.")
    os._exit(0)  # El hijo termina

else:  # Código del proceso padre
    print(f"- [Proceso Padre] PID: {os.getpid()} --> No llamaré a wait() aún.")
    print(f"- [Proceso Padre] --> Revisa el proceso zombi con: ps -el | grep {pid} o ps -el | grep Z")
    
    time.sleep(20)  # Espera para permitir que el hijo se observe como zombi

    print(f"- [Proceso Padre] --> Ahora recojo el estado del hijo (PID: {pid})...")
    os.wait()  # Aquí el padre recoge el estado del hijo
    print("- [Proceso Padre] --> Proceso hijo recogido, ya no es un zombi.")
