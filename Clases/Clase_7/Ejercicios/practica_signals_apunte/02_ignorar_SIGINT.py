import signal
import time

def default_handler(signum, frame):
    print("⚠️ Ahora el programa terminará si presionás Ctrl+C")

# Ignorar SIGINT durante 10 segundos
signal.signal(signal.SIGINT, signal.SIG_IGN)
print("🙈 Ignorando Ctrl+C por 10 segundos...")
time.sleep(10)

# Restaurar el handler por defecto
signal.signal(signal.SIGINT, default_handler)
print("🔁 SIGINT ahora se maneja con un handler personalizado.")

while True:
    time.sleep(1)