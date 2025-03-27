"""Ejercicio 4: Secuencia controlada de procesos"""
# Diseña un programa donde se creen dos hijos de manera secuencial: se lanza el primero, 
# se espera a que finalice, y luego se lanza el segundo. Cada hijo debe realizar una tarea mínima.

import os
import time

def crear_hijo(nombre):
    pid = os.fork()
    
    if pid == 0:
        print(f"--> Se creo el Proceso Hijo {nombre} - PID: {os.getpid()}")
        time.sleep(3) #tarea minima
        print(f"Proceso Hijo {nombre} ha terminado.")
        time.sleep(1)
        os._exit(0)
    else:
        os.wait()

crear_hijo("A")
crear_hijo("B")
print(f"-->v [Padre] Se han creado los dos hijos.")