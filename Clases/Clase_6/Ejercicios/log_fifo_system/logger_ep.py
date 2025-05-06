# logger_ep.py
import time

# Abre el FIFO en modo escritura
with open('/tmp/log_fifo2', 'w') as fifo:
    while True:
        mensaje = input("Escribe el mensaje de log (o 'salir' para terminar): ")
        if mensaje.lower() == 'salir':
            break
        # Escribe el mensaje en el FIFO
        fifo.write(mensaje + '\n')
        fifo.flush()  # Asegura que el mensaje se escriba inmediatamente
        time.sleep(1)  # Simula un retraso entre los mensajes
