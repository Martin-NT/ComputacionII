# emisor.py
while True:
    mensaje = input("Escribe tu mensaje: ")
    with open('/tmp/chat_in', 'w') as fifo_in:
        fifo_in.write(mensaje + '\n')
    with open('/tmp/chat_out', 'r') as fifo_out:
        respuesta = fifo_out.readline().strip()
        print("Respuesta: ", respuesta)
        
