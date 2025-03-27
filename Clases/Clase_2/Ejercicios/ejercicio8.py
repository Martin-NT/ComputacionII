"""Ejercicio 8: Simulación de servidor multiproceso"""
# Imita el comportamiento de un servidor concurrente que atiende múltiples clientes creando 
# un proceso hijo por cada uno. Cada proceso debe simular la atención a un cliente con un `sleep()`.
    
import os
import time

# Función que simula la atención a un cliente
def atender_cliente(n):
    pid = os.fork()  # Crear un proceso hijo

    if pid == 0:  # Bloque de código que se ejecuta en el proceso hijo
        print(f"[HIJO {n}] Atendiendo cliente...")  # El hijo simula atender a un cliente
        print("----------------------------------------------------------------------------------------------")
        time.sleep(2)  # Simula un tiempo de atención de 2 segundos
        print(f"[HIJO {n}] Finalizado.")  # El hijo informa que terminó de atender al cliente
        print("----------------------------------------------------------------------------------------------")
        os._exit(0)  # El hijo termina su ejecución

# Crear 5 hijos para simular la atención de 5 clientes
for cliente in range(5):
    atender_cliente(cliente)

# El proceso padre espera a que todos los hijos terminen
for _ in range(5):
    os.wait()  # El padre espera que cada hijo termine
