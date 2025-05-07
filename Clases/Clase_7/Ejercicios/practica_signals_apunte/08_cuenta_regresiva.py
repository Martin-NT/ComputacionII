import os
import signal
import time

contador = 3

def manejador(signum, frame):
    global contador
    print(f"🔔 Señal recibida. Cuenta: {contador}")
    contador -= 1

def hijo():
    signal.signal(signal.SIGUSR1, manejador)
    print(f"👶 Hijo esperando señales (PID={os.getpid()})")
    for _ in range(3):
        signal.pause()
    print("✅ ¡Cuenta regresiva terminada!")

def padre(pid_hijo):
    for i in range(3):
        time.sleep(1)
        print(f"📨 Enviando señal {i+1}...")
        os.kill(pid_hijo, signal.SIGUSR1)

if __name__ == '__main__':
    pid = os.fork()
    if pid == 0:
        hijo()
    else:
        padre(pid)
