### Ejercicio 4: Simulador de Shell

#Implementa un programa que simule una versión simplificada del operador pipe (|) de la shell. El programa debe ejecutar dos comandos 
# proporcionados por el usuario y conectar la salida del primero con la entrada del segundo.

# python3 4.simulador_de_shell.py
import os
import sys
import subprocess

def simulate_pipe(cmd1, cmd2):
    """
    Simula el operador pipe (|) de la shell conectando
    la salida de cmd1 con la entrada de cmd2.
    """
    # Crear un pipe
    read_fd, write_fd = os.pipe()
    
    # Bifurcar para el primer comando
    pid1 = os.fork()
    
    if pid1 == 0:  # Proceso hijo para cmd1
        # Redirigir stdout al extremo de escritura del pipe
        os.close(read_fd)  # Cerrar el extremo de lectura que no usamos
        os.dup2(write_fd, sys.stdout.fileno())  # Redirigir stdout
        os.close(write_fd)  # Cerrar el descriptor original ahora que está duplicado
        
        # Ejecutar el primer comando
        try:
            cmd1_parts = cmd1.split()
            os.execvp(cmd1_parts[0], cmd1_parts)
        except Exception as e:
            print(f"Error executing {cmd1}: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Bifurcar para el segundo comando
    pid2 = os.fork()
    
    if pid2 == 0:  # Proceso hijo para cmd2
        # Redirigir stdin al extremo de lectura del pipe
        os.close(write_fd)  # Cerrar el extremo de escritura que no usamos
        os.dup2(read_fd, sys.stdin.fileno())  # Redirigir stdin
        os.close(read_fd)  # Cerrar el descriptor original ahora que está duplicado
        
        # Ejecutar el segundo comando
        try:
            cmd2_parts = cmd2.split()
            os.execvp(cmd2_parts[0], cmd2_parts)
        except Exception as e:
            print(f"Error executing {cmd2}: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Proceso padre: cerrar ambos extremos del pipe y esperar
    os.close(read_fd)
    os.close(write_fd)
    
    # Esperar a que ambos procesos terminen
    os.waitpid(pid1, 0)
    os.waitpid(pid2, 0)



def main():
    print("Simulador de Pipes de Shell")
    print("Ingrese 'exit' para salir")
    print("Ejemplo: ls -l | grep .py")
    
    while True:
        try:
            user_input = input("\n$ ")
            
            if user_input.lower() == 'exit':
                break
            
            # Verificar si el input contiene el operador pipe
            if '|' not in user_input:
                print("Error: Debe incluir el operador '|' para conectar dos comandos")
                continue
            
            # Dividir la entrada en dos comandos
            cmd1, cmd2 = [cmd.strip() for cmd in user_input.split('|', 1)]
            
            if not cmd1 or not cmd2:
                print("Error: Debe proporcionar dos comandos válidos")
                continue
            
            print(f"Ejecutando: '{cmd1}' | '{cmd2}'")
            simulate_pipe(cmd1, cmd2)
            
        except KeyboardInterrupt:
            print("\nInterrumpido por el usuario")
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("Saliendo del simulador")

if __name__ == "__main__":
    main()
    
"""
**Explicación:**
1. Creamos un programa interactivo que simula el operador pipe (|) de la shell UNIX.
2. La función principal:
   - Solicita al usuario comandos separados por |
   - Divide el input en dos comandos (antes y después del |)
   - Llama a simulate_pipe() para ejecutar los comandos conectados
3. La función simulate_pipe():
   - Crea un pipe usando os.pipe()
   - Bifurca dos procesos hijos, uno para cada comando
   - Usa os.dup2() para redirigir stdout del primer proceso al pipe
   - Usa os.dup2() para redirigir stdin del segundo proceso desde el pipe
   - Usa os.execvp() para ejecutar los comandos del sistema
4. Implementamos manejo de errores y una forma de salir del programa.

Este ejercicio proporciona una visión profunda de cómo funciona realmente el operador pipe (|) en las shells UNIX, 
demostrando técnicas avanzadas como la redirección de descriptores de archivo y la ejecución de programas externos.
"""

"""
Simulador de Pipes de Shell
Ingrese 'exit' para salir
Ejemplo: ls -l | grep .py

$ ls -l | grep .py
Ejecutando: 'ls -l' | 'grep .py'
-rw-rw-r-- 1 martin martin  3318 abr  9 11:16 1.eco_simple.py
-rw-rw-r-- 1 martin martin  5352 abr  9 12:50 2.contador_de_palabras.py
-rw-rw-r-- 1 martin martin  5949 abr  9 12:51 3.pipeline_de_filtrado.py
-rw-rw-r-- 1 martin martin  4172 abr  9 12:53 4.simulador_de_shell.py
-rw-rw-r-- 1 martin martin   234 abr  9 11:24 5.chat_bidireccional.py
-rw-rw-r-- 1 martin martin   326 abr  9 11:25 6.servidor_operaciones_matematicas.py
-rw-rw-r-- 1 martin martin   467 abr  9 11:25 7.sistema_procesamiento_transacciones.py
-rw-rw-r-- 1 martin martin   980 abr  8 10:23 pipe_basico.py
-rw-rw-r-- 1 martin martin   837 abr  8 10:28 pipe_bidireccional.py
-rw-rw-r-- 1 martin martin   684 abr  8 10:25 pipe_multiprocessing.py
-rw-rw-r-- 1 martin martin  1323 abr  8 10:27 pipe_pipeline.py

$ exit
Saliendo del simulador

"""