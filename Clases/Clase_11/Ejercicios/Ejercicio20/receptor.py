#Este proceso espera indefinidamente y responde a señales SIGUSR1 y SIGUSR2 
# con acciones diferentes.
import signal
import time
import sys

def manejador_sigusr1(signum, frame):
    print("Recibí SIGUSR1: acción A")

def manejador_sigusr2(signum, frame):
    print("Recibí SIGUSR2: acción B")

def main():
    signal.signal(signal.SIGUSR1, manejador_sigusr1)
    signal.signal(signal.SIGUSR2, manejador_sigusr2)

    print(f"PID receptor: {os.getpid()}. Esperando señales...")
    try:
        while True:
            signal.pause()  # Espera indefinidamente hasta recibir señal
    except KeyboardInterrupt:
        print("\nFinalizando receptor.")
        sys.exit(0)

if __name__ == "__main__":
    import os
    main()
