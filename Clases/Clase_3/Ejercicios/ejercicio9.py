"""Ejercicio 9: Detección de procesos zombis en el sistema"""
# Escribe un script que recorra `/proc` y detecte procesos en estado zombi,
# listando su PID, PPID y nombre del ejecutable. Este ejercicio debe realizarse sin utilizar `ps`.

import os

def detectar_zombis():
    zombi_detectado = False  # Variable para verificar si se detectó algún zombi
    
    # Recorremos todos los directorios dentro de /proc (cada directorio corresponde a un PID)
    for pid in os.listdir('/proc'):
        if pid.isdigit():  # Solo consideramos los directorios cuyo nombre es un número (PID válidos)
            try:
                # Abrimos el archivo /proc/{pid}/status para leer el estado del proceso
                with open(f"/proc/{pid}/status") as f:
                    lines = f.readlines()
                    
                    # Buscamos el estado del proceso
                    estado = next((l for l in lines if l.startswith("State:")), "")
                    if "Z" in estado:  # Si el estado es "Z", el proceso está en estado zombi
                        # Obtenemos el nombre del proceso y el PPID
                        nombre = next((l for l in lines if l.startswith("Name:")), "").split()[1]
                        ppid = next((l for l in lines if l.startswith("PPid:")), "").split()[1]
                        # Imprimimos la información del proceso zombi
                        print(f"--> Zombi detectado → PID: {pid}, PPID: {ppid}, Nombre: {nombre}")
                        zombi_detectado = True  # Marcamos que se detectó un zombi
            except IOError:
                continue
    
    # Si no se detectaron zombis, imprimimos un mensaje
    if not zombi_detectado:
        print("--> No se detectaron procesos zombis en el sistema.")

# Llamamos a la función para detectar procesos zombis
detectar_zombis()

"""Para hacer la prueba de zombis, puedes ejecutar el siguiente script en la terminal:"""

"""--> Si queres un zombi, ejecuta en otra terminal:"""
# python3 proceso_zombie.py 

"""--> Si no queres un zombi, ejecuta en otra terminal:"""
# python3 ejercicio9.py