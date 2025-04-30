from multiprocessing import Process, Lock
import time

# Simulando una cuenta bancaria
class CuentaBancaria:
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial

    def actualizar_saldo(self, cantidad, lock):
        # Usamos el lock para asegurarnos que no haya acceso concurrente
        with lock:
            tiempo = time.sleep(0.1)  # Simulando algo de trabajo
            self.saldo += cantidad
            print(f"Saldo actualizado: {self.saldo}")

def operacion(cuenta, lock, cantidad):
    cuenta.actualizar_saldo(cantidad, lock)

if __name__ == "__main__":
    cuenta = CuentaBancaria(100)
    lock = Lock()

    procesos = [
        Process(target=operacion, args=(cuenta, lock, 50)),
        Process(target=operacion, args=(cuenta, lock, -30))
    ]

    for p in procesos:
        p.start()

    for p in procesos:
        p.join()

    print("Operación finalizada.")
