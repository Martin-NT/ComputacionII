from multiprocessing import Pipe, Process

# Función que se ejecutará en el proceso hijo
def child_process(conn):
    conn.send("Hola desde el hijo!")  # Enviar un mensaje (string)
    conn.close()  # Cerrar el extremo de conexión después de enviar

if __name__ == "__main__":
    # Crear un pipe con dos extremos de conexión
    parent_conn, child_conn = Pipe()

    # Crear y lanzar un proceso hijo, pasándole un extremo del pipe
    p = Process(target=child_process, args=(child_conn,))
    p.start()

    # El padre recibe el mensaje que envió el hijo
    mensaje = parent_conn.recv()
    print("Padre recibió:", mensaje)

    # Esperar a que el hijo termine
    p.join()
