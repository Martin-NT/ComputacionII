import os
import signal
import time

# Bandera global
detener = False

def handler(signum, frame):
    global detener
    detener = True  # ✅ Solo cambia un flag

def proceso():
    signal.signal(signal.SIGUSR1, handler)
    print("🕰️ Esperando SIGUSR1 para detenerme...")
    while not detener:
        print("... trabajando ...")
        time.sleep(1)
    print("🚨 Señal recibida. Deteniéndose con gracia.")

if __name__ == '__main__':
    pid = os.fork()
    if pid == 0:
        proceso()
    else:
        time.sleep(3)
        os.kill(os.getpid() + 1, signal.SIGUSR1)  # Envia señal al hijo
