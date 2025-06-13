import os
import time
import random

def hijo(nombre, duracion):
    print(f"- [{nombre}] PID {os.getpid()} - durmiendo {duracion} segundos.")
    time.sleep(duracion)
    print(f"--> [{nombre}] PID {os.getpid()} - finalizando.")
    os._exit(0)  # Salida explícita sin excepciones

def main():
    hijos = []
    nombres = ["H1", "H2", "H3"]

    # Crear hijos
    for nombre in nombres:
        duracion = random.randint(1, 5)
        pid = os.fork()
        if pid == 0:
            hijo(nombre, duracion)
        else:
            hijos.append(pid)

    # Recolección manual con waitpid
    print(f"--> [Padre] Esperando finalización de hijos...")
    terminados = []

    while hijos:
        pid, estado = os.waitpid(-1, 0)
        if os.WIFEXITED(estado):
            exit_code = os.WEXITSTATUS(estado)
            terminados.append((pid, exit_code))
            print(f"-->[Padre] Hijo PID {pid} terminó con exit {exit_code}.")
            hijos.remove(pid)

    print("\nOrden de finalización:")
    for pid, code in terminados:
        print(f" - Hijo PID {pid} terminó con código {code}")

if __name__ == "__main__":
    main()
