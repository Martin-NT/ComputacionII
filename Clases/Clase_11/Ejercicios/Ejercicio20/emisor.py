#Este proceso envía señales SIGUSR1 y SIGUSR2 alternadamente al receptor cada 3 segundos.
import os
import signal
import time
import sys

def main():
    if len(sys.argv) != 2:
        print(f"Uso: python3 {sys.argv[0]} <PID_receptor>")
        sys.exit(1)

    pid_receptor = int(sys.argv[1])
    señales = [signal.SIGUSR1, signal.SIGUSR2]
    idx = 0

    print(f"Enviando señales a PID {pid_receptor}...")

    try:
        while True:
            sig = señales[idx % 2]
            os.kill(pid_receptor, sig)
            print(f"Envié señal: {sig.name}")
            idx += 1
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nFinalizando emisor.")
        sys.exit(0)

if __name__ == "__main__":
    main()
