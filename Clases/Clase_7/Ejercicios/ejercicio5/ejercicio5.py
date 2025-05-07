import signal
import os
import time
import queue

# Cola de trabajos
job_queue = queue.Queue()

# Handler para SIGUSR1
def handle_job(signum, frame):
    global job_queue
    print("Trabajo recibido. Procesando...")
    job_queue.put(time.time())

# Procesar trabajos
def process_jobs():
    while True:
        if not job_queue.empty():
            job = job_queue.get()
            print(f"Procesando trabajo: {job}")
            time.sleep(2)

# Crear el proceso productor
def producer():
    while True:
        os.kill(os.getppid(), signal.SIGUSR1)  # Enviar trabajo
        time.sleep(1)

# Configurar señales
signal.signal(signal.SIGUSR1, handle_job)

# Crear procesos
pid = os.fork()
if pid == 0:  # Hijo: consumidor
    process_jobs()
else:  # Padre: productor
    producer()
