from multiprocessing import Process, current_process

def hijo():
    print(f"[Hijo] PID: {current_process().pid}")

if __name__ == '__main__':
    procesos = [Process(target=hijo) for _ in range(2)]
    for p in procesos:
        p.start()
    for p in procesos:
        p.join()
    print('[Padre] Hijos finalizados — PID padre:', current_process().pid)