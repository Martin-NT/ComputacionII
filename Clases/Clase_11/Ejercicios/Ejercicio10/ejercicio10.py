import multiprocessing
import time
import random
import os

class CuentaBancaria:
    def __init__(self, saldo_inicial, lock):
        self.saldo = multiprocessing.Value('i', saldo_inicial)
        self.lock = lock

    def depositar(self, cantidad):
        with self.lock:
            self._actualizar_saldo(cantidad, "depositar")

    def retirar(self, cantidad):
        with self.lock:
            if self.saldo.value >= cantidad:
                self._actualizar_saldo(-cantidad, "retirar")
            else:
                print(f"PID {os.getpid()} - Saldo insuficiente para retirar {cantidad}")

    def _actualizar_saldo(self, cambio, operacion):
        # Método también sincronizado (llamado desde otros métodos con el lock ya tomado)
        with self.lock:
            pid = os.getpid()
            print(f"PID {pid} - {operacion} {abs(cambio)} | Saldo antes: {self.saldo.value}")
            self.saldo.value += cambio
            print(f"PID {pid} - Saldo después: {self.saldo.value}")

def operacion_bancaria(cuenta):
    # Cada proceso realiza depósitos o retiros aleatorios
    for _ in range(5):
        if random.choice([True, False]):
            cuenta.depositar(random.randint(10, 50))
        else:
            cuenta.retirar(random.randint(10, 50))
        time.sleep(random.uniform(0.1, 0.5))

def main():
    lock = multiprocessing.RLock()  # Reentrant lock
    cuenta = CuentaBancaria(100, lock)

    procesos = []
    for _ in range(4):
        p = multiprocessing.Process(target=operacion_bancaria, args=(cuenta,))
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()

    print(f"\nSaldo final: {cuenta.saldo.value}")

if __name__ == "__main__":
    main()