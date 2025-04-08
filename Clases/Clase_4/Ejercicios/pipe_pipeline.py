from multiprocessing import Pipe, Process

# Proceso 1: envía un número
def productor(conn):
    conn.send(10)         # Enviar el número 10 al siguiente proceso
    conn.close()          # Cerrar la conexión al terminar

# Proceso 2: recibe el número, lo procesa y lo reenvía
def procesador(conn_in, conn_out):
    numero = conn_in.recv()     # Recibir número del productor
    resultado = numero * 2      # Procesar: multiplicar por 2
    conn_out.send(resultado)    # Enviar el resultado al consumidor
    conn_in.close()
    conn_out.close()

# Proceso 3: recibe y muestra el resultado
def consumidor(conn):
    resultado = conn.recv()     # Recibir el resultado final
    print("Resultado final:", resultado)
    conn.close()

if __name__ == "__main__":
    # Pipe entre productor y procesador
    p1_conn_out, p1_conn_in = Pipe()

    # Pipe entre procesador y consumidor
    p2_conn_out, p2_conn_in = Pipe()

    # Crear procesos y conectarlos con los extremos correspondientes
    p1 = Process(target=productor, args=(p1_conn_in,))
    p2 = Process(target=procesador, args=(p1_conn_out, p2_conn_in))
    p3 = Process(target=consumidor, args=(p2_conn_out,))

    # Iniciar los procesos
    p1.start()
    p2.start()
    p3.start()

    # Esperar a que todos terminen
    p1.join()
    p2.join()
    p3.join()
