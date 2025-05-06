# receptor.py
while True:
    with open('/tmp/chat_in', 'r') as fifo_in:
        mensaje = fifo_in.readline().strip()
        print("Mensaje recibido: ", mensaje)
        respuesta = input("Escribe tu respuesta: ")
    with open('/tmp/chat_out', 'w') as fifo_out:
        fifo_out.write(respuesta + '\n')

# Recorda crear los fifos: mkfifo /tmp/chat_in /tmp/chat_out