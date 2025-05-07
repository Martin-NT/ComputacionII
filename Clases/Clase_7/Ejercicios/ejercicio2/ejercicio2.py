import signal
import os
import random
import time

# Handler para todas las señales
def handle_signals(signum, frame):
    pid = os.getpid()
    ppid = os.getppid()
    print(f"Recibida señal {signum} del hijo {frame.f_globals['__pid__']}")

# Crear 3 procesos hijos
def create_child(signal_type):
    pid = os.fork()
    if pid == 0:  # Hijo
        time.sleep(random.randint(1, 3))  # Retardo aleatorio
        os.kill(os.getppid(), signal_type)
        exit(0)
    else:
        return pid

# Registrar el handler
signal.signal(signal.SIGUSR1, handle_signals)
signal.signal(signal.SIGUSR2, handle_signals)
signal.signal(signal.SIGTERM, handle_signals)

# Lanzar 3 procesos hijos con diferentes señales
print("Padre en ejecución...")
for i, signal_type in enumerate([signal.SIGUSR1, signal.SIGUSR2, signal.SIGTERM]):
    create_child(signal_type)
    
# Esperar que los hijos terminen
while True:
    pass
