import signal
import os
import time

# Manejador personalizado para SIGUSR1
def manejar_sigusr1(signum, frame):
    print(f"\nSeñal SIGUSR1 recibida por el proceso {os.getpid()}")

def main():
    print(f"Proceso PID: {os.getpid()}")
    print("Esperando señal SIGUSR1...")

    # Instalar el manejador
    signal.signal(signal.SIGUSR1, manejar_sigusr1)

    # Espera pasiva
    while True:
        time.sleep(1)  # Mantiene el proceso vivo sin consumir CPU

if __name__ == "__main__":
    main()
