import os
import signal
import time

def handler(signum, frame):
    print("✅ Hijo recibió SIGINT. Puede continuar.")

def hijo():
    signal.signal(signal.SIGINT, handler)
    print(f"👶 Hijo esperando SIGINT (PID={os.getpid()})")
    signal.pause()
    print("🚀 Hijo continúa.")

def padre(pid_hijo):
    time.sleep(2)
    print(f"📨 Padre envía SIGINT al hijo (PID={pid_hijo})")
    os.kill(pid_hijo, signal.SIGINT)

if __name__ == '__main__':
    pid = os.fork()
    if pid == 0:
        hijo()
    else:
        padre(pid)
