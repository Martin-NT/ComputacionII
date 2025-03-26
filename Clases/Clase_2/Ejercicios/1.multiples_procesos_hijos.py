#📌 Objetivo: Crear tres procesos hijos desde un mismo padre. Cada uno imprimirá su PID y luego terminará.

import os

for i in range(3):  # Crear 3 procesos hijos
    pid = os.fork()
    if pid == 0:  # Código del hijo
        print(f"Soy el hijo {i} con PID {os.getpid()}, mi padre es {os.getppid()}")
        exit(0)  # Terminar el hijo inmediatamente

# Solo el padre llega aquí
for i in range(3):  
    os.wait()  # Esperar a los 3 hijos
print("Todos los hijos han terminado, padre finalizando.")

#🔍 ¿Qué observar?
#   Se crean tres hijos, cada uno con un PID distinto.
#   El padre espera a que todos los hijos terminen antes de finalizar.