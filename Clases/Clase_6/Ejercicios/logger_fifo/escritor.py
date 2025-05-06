# escritor.py
mensaje = input("Mensaje a registrar: ")

with open('/tmp/log_fifo', 'w') as fifo:
    fifo.write(mensaje + '\n')
