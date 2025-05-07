import os
import signal
import time

def manejador_usr1(signum, frame):
    print("🟢 Hijo recibió SIGUSR1: Acción A")

def manejador_usr2(signum, frame):
    print("🔵 Hijo recibió SIGUSR2: Acción B")

def hijo():
    signal.signal(signal.SIGUSR1, manejador_usr1)
    signal.signal(signal.SIGUSR2, manejador_usr2)
    print(f"👶 Hijo esperando señales (PID={os.getpid()})")
    for _ in range(2):
        signal.pause()
    print("🏁 Hijo terminó.")

def padre(pid_hijo):
    time.sleep(1)
    print("📨 Enviando SIGUSR1...")
    os.kill(pid_hijo, signal.SIGUSR1)
    time.sleep(1)
    print("📨 Enviando SIGUSR2...")
    os.kill(pid_hijo, signal.SIGUSR2)

if __name__ == '__main__':
    pid = os.fork()
    if pid == 0:
        hijo()
    else:
        padre(pid)
