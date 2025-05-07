import os
import signal
import time

# Señal
def manejador_usr1(signum, frame):
    print("📩 Señal SIGUSR1 recibida.")

def proceso_con_pipe():
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        # Hijo
        os.close(w)
        msg = os.read(r, 100).decode()
        print(f"👶 Hijo leyó del pipe: {msg}")
        os._exit(0)
    else:
        os.close(r)
        os.write(w, b"Hola desde el padre")
        os.wait()

if __name__ == "__main__":
    # Señales
    print(f"PID actual: {os.getpid()}")
    signal.signal(signal.SIGUSR1, manejador_usr1)
    os.kill(os.getpid(), signal.SIGUSR1)
    time.sleep(1)

    print("\n--- Comunicación por pipe ---")
    proceso_con_pipe()
