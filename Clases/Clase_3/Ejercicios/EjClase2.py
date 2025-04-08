"""Ejercicio 2: Doble bifurcación"""
# Escribe un programa donde un proceso padre cree dos hijos diferentes (no en cascada), 
# y cada hijo imprima su identificador. El padre deberá esperar a que ambos terminen.

import os
import time

for i in range(2):
    pid = os.fork()
    
    if pid == 0:  
        print(f"[Proceso Hijo {i}] PID: {os.getpid()} - Proceso Padre: {os.getppid()}")
        time.sleep(3)  
        os._exit(0)  # Finaliza el proceso hijo


for _ in range(2):
    pid_hijo, status = os.wait()  # Espera a que un hijo termine
    print(f"--> El Proceso Hijo con PID {pid_hijo} ha terminado.")
    time.sleep(2)  # Espera antes de permitir que termine el siguiente hijo

print("--> Todos los hijos han terminado, el padre finaliza.")

