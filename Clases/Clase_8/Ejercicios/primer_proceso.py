from multiprocessing import Process
import os

def worker():
    print(f"Proceso hijo con PID: {os.getpid()}")

if __name__ == '__main__':
    print(f"Proceso padre con PID: {os.getpid()}")
    p = Process(target=worker)
    p.start()
    p.join()
