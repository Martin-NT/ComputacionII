from multiprocessing import Pipe, Process

# Proceso hijo: recibe un mensaje y responde
def hijo(conn):
    # Esperar mensaje del padre
    mensaje = conn.recv()
    print("Hijo recibió:", mensaje)

    # Preparar y enviar respuesta
    respuesta = f"Recibido: {mensaje}"
    conn.send(respuesta)

    conn.close()  # Cerrar la conexión

if __name__ == "__main__":
    # Crear un pipe bidireccional (por defecto duplex=True)
    padre_conn, hijo_conn = Pipe()

    # Crear proceso hijo y pasarle un extremo del pipe
    p = Process(target=hijo, args=(hijo_conn,))
    p.start()

    # Padre envía un mensaje al hijo
    padre_conn.send("Hola hijo, ¿me escuchás?")

    # Esperar respuesta del hijo
    respuesta = padre_conn.recv()
    print("Padre recibió respuesta:", respuesta)

    # Esperar a que el hijo termine
    p.join()
