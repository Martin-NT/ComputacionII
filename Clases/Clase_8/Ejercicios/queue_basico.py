from multiprocessing import Process, Queue

def hijo(cola):
    cola.put("Mensaje desde el hijo")

if __name__ == '__main__':
    cola = Queue()
    p = Process(target=hijo, args=(cola,))
    p.start()

    print("[Padre] Esperando mensaje...")
    mensaje = cola.get()
    print(f"[Padre] Recibido: {mensaje}")

    p.join()
