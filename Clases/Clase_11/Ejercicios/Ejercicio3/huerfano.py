import os
import time

def crear_huerfano():
    pid = os.fork()

    if pid == 0:
        # Hijo
        time.sleep(1)  # Espera a que el padre termine
        print(f"[Hijo] PID={os.getpid()}, PPID actual={os.getppid()}")
        time.sleep(40)  # Se mantiene vivo para inspección
        print("[Hijo] Terminando.")
    else:
        # Padre
        print(f"[Padre] PID={os.getpid()}, creó al hijo PID={pid}")
        print("[Padre] Terminando inmediatamente.")
        os._exit(0)

if __name__ == "__main__":
    crear_huerfano()