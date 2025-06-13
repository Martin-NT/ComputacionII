import argparse
import os
import time
import random
import multiprocessing
import subprocess

def tarea_hijo(verbose):
    pid = os.getpid()
    ppid = os.getppid()
    duracion = random.randint(1, 5)
    
    if verbose:
        print(f"[Hijo PID={pid}] Iniciado. Padre PID={ppid}. Durmiendo {duracion} segundos...")
    
    time.sleep(duracion)
    
    if verbose:
        print(f"[Hijo PID={pid}] Terminando.")

def main():
    parser = argparse.ArgumentParser(description="Gestor de procesos hijos.")
    parser.add_argument("--num", type=int, required=True, help="Número de procesos hijos a crear.")
    parser.add_argument("--verbose", action="store_true", help="Mostrar mensajes detallados.")
    
    args = parser.parse_args()

    print(f"[Padre PID={os.getpid()}] Creando {args.num} procesos hijos...")

    procesos = []
    for i in range(args.num):
        p = multiprocessing.Process(target=tarea_hijo, args=(args.verbose,))
        procesos.append(p)
        p.start()

    # Mostrar jerarquía de procesos usando pstree -p
    print("\n[Padre] Jerarquía de procesos (pstree -p):")
    subprocess.run(["pstree", "-p", str(os.getpid())])

    for p in procesos:
        p.join()

    print(f"[Padre PID={os.getpid()}] Todos los procesos hijos han terminado.")

if __name__ == "__main__":
    main()
