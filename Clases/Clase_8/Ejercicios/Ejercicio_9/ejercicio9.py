import time
import random
from multiprocessing import Process, Value, Lock

# Simulación de la operación del cajero: Retiro o depósito
def cajero(operacion, monto, balance, lock, reintentos):
    intentos = 0
    while True:
        with lock:
            # Si la operación es retiro y el monto es mayor al balance, no hacer nada
            if operacion == "retirar" and balance.value >= monto:
                balance.value -= monto
                print(f"Cajero {operacion}: Retirado {monto}, nuevo balance: {balance.value}")
                break
            elif operacion == "depositar":
                balance.value += monto
                print(f"Cajero {operacion}: Depositado {monto}, nuevo balance: {balance.value}")
                break
            else:
                # Si no se puede realizar la operación, incrementamos los intentos y aplicamos el backoff
                intentos += 1
                if intentos >= reintentos:
                    print(f"Operación fallida después de {intentos} intentos.")
                    break
                # Aplicamos la política de backoff exponencial
                time.sleep(random.uniform(0, 2 ** intentos))  # Espera exponencial

def simulacion_banco(num_cajeros, balance_inicial, reintentos):
    balance = Value('d', balance_inicial)  # Balance compartido
    lock = Lock()  # Sincronización para el acceso al balance
    
    cajeros_procesos = []
    
    # Simulamos múltiples cajeros
    for i in range(num_cajeros):
        operacion = random.choice(["depositar", "retirar"])
        monto = random.uniform(10, 100)
        proceso = Process(target=cajero, args=(operacion, monto, balance, lock, reintentos))
        cajeros_procesos.append(proceso)
    
    # Iniciar los procesos
    for proceso in cajeros_procesos:
        proceso.start()
    
    # Esperar a que todos los procesos terminen
    for proceso in cajeros_procesos:
        proceso.join()

if __name__ == "__main__":
    num_cajeros = 5  # Número de cajeros (procesos)
    balance_inicial = 500  # Balance inicial
    reintentos = 5  # Máximo número de intentos antes de abortar

    simulacion_banco(num_cajeros, balance_inicial, reintentos)
