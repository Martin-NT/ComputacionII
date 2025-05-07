import os
import signal
import time

# Flag de emergencia
apagado_emergencia = False

def handler_apagado(signum, frame):
    global apagado_emergencia
    apagado_emergencia = True  # 🚨 El handler solo cambia el estado

def simulador_motor():
    signal.signal(signal.SIGUSR2, handler_apagado)
    print(f"🔧 Simulando motor en ejecución. PID: {os.getpid()}")

    while not apagado_emergencia:
        print("⚙️ Motor funcionando normalmente...")
        time.sleep(1)

    print("🛑 Apagado de emergencia activado. Deteniendo motor.")

if __name__ == '__main__':
    simulador_motor()
