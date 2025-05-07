import os
import signal
import time

def esperar_senal(signum, frame):
    print("✅ Hijo recibió señal. Puede continuar.")

def hijo():
    signal.signal(signal.SIGUSR1, esperar_senal)
    print(f"👶 Hijo esperando señal SIGUSR1 (PID={os.getpid()})")
    signal.pause()  # Espera pasivamente la señal
    print("🚀 Hijo continúa con su tarea.")

def padre(pid_hijo):
    print(f"👨 Padre (PID={os.getpid()}) esperando 3 segundos...")
    time.sleep(3)
    print(f"📨 Enviando SIGUSR1 al hijo (PID={pid_hijo})")
    os.kill(pid_hijo, signal.SIGUSR1)

if __name__ == '__main__':
    pid = os.fork()
    if pid == 0:
        hijo()
    else:
        padre(pid)
