import signal
import threading
import time

# Variables globales
counter = 30
lock = threading.Lock()
pause = False

# Función para contar
def count_down():
    global counter, pause
    while counter > 0:
        time.sleep(1)
        with lock:
            if not pause:
                counter -= 1
                print(f"Cuenta regresiva: {counter}")

# Manejadores de señales
def pause_count(signum, frame):
    global pause
    with lock:
        pause = True
    print("Cuenta pausada.")

def resume_count(signum, frame):
    global pause
    with lock:
        pause = False
    print("Cuenta reanudada.")

# Registrar los handlers de señales
signal.signal(signal.SIGUSR1, pause_count)
signal.signal(signal.SIGUSR2, resume_count)

# Crear el hilo
thread = threading.Thread(target=count_down)
thread.start()

# Esperar señales
print("Hilo de cuenta regresiva en ejecución...")
while True:
    time.sleep(1)
