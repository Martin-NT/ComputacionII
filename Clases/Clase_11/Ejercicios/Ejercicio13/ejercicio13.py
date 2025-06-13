import multiprocessing
import os
import time

def hijo():
    print(f"Hijo PID {os.getpid()} | Padre PID {os.getppid()}")
    time.sleep(20)  # el hijo se mantiene vivo unos segundos para poder inspeccionarlo

def main():
    print(f"Padre PID {os.getpid()} creando hijos...")

    p1 = multiprocessing.Process(target=hijo)
    p2 = multiprocessing.Process(target=hijo)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Padre finaliza.")

if __name__ == "__main__":
    main()
