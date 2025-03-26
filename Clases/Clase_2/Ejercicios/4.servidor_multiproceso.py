#📌 Objetivo: Aplicar lo aprendido creando un servidor multiproceso que maneje clientes con fork().
#   -Crear un servidor TCP que acepte múltiples clientes.
#   -Cada cliente será manejado por un proceso hijo separado usando fork().


import os
import socket #Permite la comunicación entre procesos a través de la red.

# 1️⃣ Función para manejar clientes
def handle_client(conn):
    print(f"Nuevo cliente conectado: {conn.getpeername()}")
    conn.sendall(b"Hola desde el servidor\n")  # Envía un mensaje al cliente
    conn.close()  # Cierra la conexión
    exit(0)  # Termina el proceso hijo

#📌 ¿Qué hace esta función?
#   -Recibe una conexión (conn) de un cliente.
#   -Imprime la dirección IP del cliente.
#   -Envía un mensaje al cliente.
#   -Cierra la conexión.
#   -Finaliza el proceso hijo con exit(0).

# 2️⃣ Crear el socket del servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Crea un socket TCP/IP (IPv4).
server.bind(("0.0.0.0", 12345)) #Asigna la IP 0.0.0.0 (todas las interfaces de red) y el puerto 12345.
server.listen(5) #Permite que hasta 5 clientes esperen conexión simultáneamente.
print("Servidor escuchando en el puerto 12345...") #Mensaje indicando que el servidor está funcionando.

# 3️⃣ Bucle infinito para aceptar clientes
while True:
    conn, addr = server.accept() #Espera que un cliente se conecte.
    pid = os.fork()
    
    # 4️⃣ Crear un proceso hijo para cada cliente
    if pid == 0:  # Código del hijo
        handle_client(conn)
    else:
        conn.close()  # El padre cierra la conexión y sigue esperando clientes
        
    #Devuelve:
    #   conn → Objeto de conexión con el cliente.
    #   addr → Dirección IP y puerto del cliente.

#✅ Ejecuta el servidor y luego en otra terminal conéctate con:
#   telnet localhost 12345

#🔍 ¿Qué observarás?
#   Cada vez que un cliente se conecta, el servidor crea un proceso hijo.
#   Los hijos manejan la conexión y luego terminan limpiamente.

#✅ Resumen del flujo del servidor
#   1) El servidor espera conexiones (server.accept()).
#   2) Cuando un cliente se conecta, el servidor usa fork() para crear un proceso hijo.
#   3) El hijo maneja la conexión y finaliza.
#   4) El padre sigue esperando más clientes.
#   5) Esto permite que el servidor atienda múltiples clientes al mismo tiempo sin bloquearse.

#Refuerzo de conceptos
#📌 1. fork() crea procesos hijos → Así cada cliente se maneja en su propio proceso independiente.
#📌 2. El padre cierra conn → Si no lo hiciera, mantendría abiertas todas las conexiones, gastando memoria.
#📌 3. Sin exit(0) en el hijo → El hijo seguiría ejecutando el código del padre, causando errores o más procesos innecesarios.