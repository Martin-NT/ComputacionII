# logger.py
with open('/tmp/log_fifo', 'r') as fifo, open('registro.log', 'a') as log:
    print("Esperando mensajes... (Ctrl+C para detener)")
    for line in fifo:
        print("Log recibido:", line.strip())
        log.write(line)

# Recorda crear el fifo: mkfifo /tmp/log_fifo
#1. Abrí una terminal y ejecutá el logger:
#python3 logger.py

#2. En otra terminal, ejecutá varias veces el escritor:
#python3 escritor.py
#📌 Verás que cada mensaje aparece por pantalla y se guarda en el archivo registro.log.