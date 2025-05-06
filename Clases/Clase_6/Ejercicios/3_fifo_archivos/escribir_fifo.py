import os

fifo_path = '/tmp/log_fifo'
with open(fifo_path, 'w') as fifo:
    while True:
        message = input("Escribe un mensaje: ")
        fifo.write(message + "\n")
        if message == "exit":
            break
