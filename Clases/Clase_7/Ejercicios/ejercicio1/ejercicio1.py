import signal
import atexit
import os
import sys

# Función de limpieza que se ejecuta al final
def cleanup():
    print("El proceso ha terminado correctamente.")

# Handler para SIGTERM
def handle_sigterm(signum, frame):
    print("Señal SIGTERM recibida.")
    cleanup()

# Registrar la función de limpieza
atexit.register(cleanup)

# Registrar el manejador para SIGTERM
signal.signal(signal.SIGTERM, handle_sigterm)

# Simulación de trabajo
print("Proceso en ejecución... Enviando SIGTERM para terminar.")
while True:
    pass  # Mantiene el proceso en ejecución
