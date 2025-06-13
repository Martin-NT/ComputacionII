import os
import time

def crear_zombi():
    pid = os.fork()

    if pid == 0:
        # Proceso hijo
        print(f"[Hijo] PID={os.getpid()} finalizando inmediatamente.")
        os._exit(0)  # Finaliza sin esperar
    else:
        # Proceso padre
        print(f"[Padre] PID={os.getpid()} - Hijo creado con PID={pid}")
        print(f"[Padre] Ejecutá: cat /proc/{pid}/status en otra terminal.")
        print("[Padre] Dormirá 10 segundos sin recolectar al hijo.")

        # Espera sin llamar a wait()
        time.sleep(10)

        # Luego recoge el estado del hijo
        os.waitpid(pid, 0)
        print(f"[Padre] Hijo {pid} recolectado.")

if __name__ == "__main__":
    crear_zombi()
