import signal
import time

# Función para manejar SIGINT
def handle_sigint(signum, frame):
    print("Señal SIGINT recibida. ¡Interrumpido!")

# Ignorar SIGINT por 5 segundos
def ignore_signal():
    print("Ignorando SIGINT por 5 segundos...")
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    time.sleep(5)
    print("Restaurando manejo de SIGINT")
    signal.signal(signal.SIGINT, handle_sigint)

# Ejecutar
ignore_signal()

# Continuar ejecutando indefinidamente
while True:
    pass
