# lector_ep.py
with open('/tmp/log_fifo2', 'r') as fifo, open('registro.log', 'a') as log_file:
    while True:
        mensaje = fifo.readline().strip()  # Lee el mensaje del FIFO
        if mensaje:  # Si hay un mensaje
            log_file.write(mensaje + '\n')  # Escribe en el archivo de log
            print(f"Mensaje de log guardado: {mensaje}")
