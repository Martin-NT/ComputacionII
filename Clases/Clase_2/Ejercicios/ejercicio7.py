"""Ejercicio 7: Multiproceso paralelo"""
# Construye un programa que cree tres hijos en paralelo (no secuenciales). 
# Cada hijo ejecutará una tarea breve y luego finalizará. El padre debe esperar por todos ellos.

import os
import time

# Crear tres hijos en paralelo
for i in range(3):
    pid = os.fork()  # Crear un proceso hijo

    if pid == 0:  # Bloque de código que se ejecuta en los hijos
        # Mostrar información sobre el hijo y su padre
        print(f"--> [HIJO {i+1}] PID: {os.getpid()}  Padre: {os.getppid()}")
        print(f"[HIJO {i+1}] Ejecutando tarea breve...")
        print("----------------------------------------------------------------------------------------------")
        
        # Simula una tarea breve (2 segundos)
        time.sleep(2)  
        
        # Imprimir el mensaje de terminación del hijo
        print(f"[HIJO {i+1}] Terminando.")
        os._exit(0)  # El hijo termina

# El padre espera que todos los hijos terminen
print("----------------------------------------------------------------------------------------------")
print("[PADRE] Esperando a que los hijos terminen...")
print("----------------------------------------------------------------------------------------------")

# El padre espera a que cada hijo termine
for _ in range(3):
    os.wait()  # El padre espera que cada hijo termine

# Mensaje final cuando todos los hijos han terminado
print("----------------------------------------------------------------------------------------------")
print("[PADRE] Todos los hijos han terminado. El proceso padre termina.")
