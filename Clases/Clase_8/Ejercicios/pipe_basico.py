from multiprocessing import Process, Pipe

def hijo(conexion_hijo):
    conexion_hijo.send("Hola desde el hijo")
    conexion_hijo.close()

if __name__ == '__main__':
    conexion_padre, conexion_hijo = Pipe()
    p = Process(target=hijo, args=(conexion_hijo,))
    p.start()

    print("[Padre] Esperando mensaje...")
    mensaje = conexion_padre.recv()
    print(f"[Padre] Recibido: {mensaje}")

    p.join()
