from multiprocessing import Process, Pipe
import random, time

def productor(conn):
    for _ in range(10):
        conn.send(random.randint(1, 100))
        time.sleep(0.1)
    conn.send(None)  # señal de fin
    conn.close()

def consumidor(conn):
    while True:
        dato = conn.recv()
        if dato is None:
            break
        print('Cuadrado:', dato**2)
    conn.close()

if __name__ == '__main__':
    p_in, c_in = Pipe()   # productor → padre
    p_out, c_out = Pipe() # padre → consumidor

    prod = Process(target=productor, args=(p_in,))
    cons = Process(target=consumidor, args=(c_out,))
    prod.start(); cons.start()

    while True:
        val = c_in.recv()
        if val is None:
            p_out.send(None)
            break
        p_out.send(val)

    prod.join(); cons.join()