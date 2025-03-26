#✅ Evita procesos zombi usando os.waitpid() en el padre.
#✅ Imprime mensajes cuando los clientes se conectan y desconectan.
#✅ Permite que el cliente envíe datos y reciba respuestas.

#1️⃣ Si el cliente escribe exit, el servidor cierra solo su conexión.
#2️⃣ Si el cliente escribe time, el servidor le envía la hora actual.
#3️⃣ Si el cliente escribe cualquier otra cosa, el servidor responde Mensaje recibido.

import os
import socket
import signal
import time

# Manejar la limpieza de procesos zombis
def clean_zombies(signum, frame):
    while True:
        try:
            pid, _ = os.waitpid(-1, os.WNOHANG)  # Limpia procesos hijos terminados
            if pid == 0:
                break
        except ChildProcessError:
            break

# Configurar el manejador de señales para evitar zombis
signal.signal(signal.SIGCHLD, clean_zombies)

# Crear el socket del servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reutilizar puerto rápidamente
server.bind(("0.0.0.0", 12345))  # Vincula el socket a la dirección IP y puerto
server.listen(5)  # El servidor puede manejar hasta 5 conexiones simultáneas
print("Servidor escuchando en el puerto 12345...")

# Función que maneja cada cliente
def handle_client(conn, addr):
    print(f"[+] Cliente conectado desde {addr}")
    
    while True:
        data = conn.recv(1024)  # Recibir datos del cliente
        if not data:
            break  # Si no hay datos, el cliente cerró la conexión
        
        # Decodificar los datos y procesar según el mensaje recibido
        try:
            message = data.decode().strip()  # Intentar decodificar los datos
            print(f"[{addr}] Cliente envió: {message}")
            
            # Verificar el comando del cliente
            if message.lower() == "exit":
                print(f"[-] Cliente {addr} desconectado por 'exit'")
                conn.sendall(b"Desconectando...\n")
                break  # Cerrar la conexión con el cliente
            elif message.lower() == "time":
                # Enviar la hora actual
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                conn.sendall(f"La hora actual es: {current_time}\n".encode())
            else:
                # Respuesta por defecto
                conn.sendall(b"Mensaje recibido\n")

        except UnicodeDecodeError:
            # Manejar error de decodificación si el mensaje no es texto válido
            print(f"[{addr}] Error al decodificar los datos recibidos: {data}")
            conn.sendall(b"Error: No se pudo procesar el mensaje recibido.\n")

    print(f"[-] Cliente {addr} desconectado")
    conn.close()
    exit(0)  # Finaliza el proceso hijo

# Aceptar conexiones en un bucle infinito
while True:
    conn, addr = server.accept()  # Espera conexión
    pid = os.fork()  # Crear proceso hijo

    if pid == 0:  # Código del hijo
        server.close()  # El hijo cierra el socket del servidor
        handle_client(conn, addr)  # Maneja la conexión
    else:  
        conn.close()  # El padre cierra la conexión y sigue esperando clientes

        
#nc localhost 12345