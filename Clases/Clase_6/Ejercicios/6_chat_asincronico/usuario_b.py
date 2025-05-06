import os
import threading
from datetime import datetime

FIFO_WRITE = '/tmp/chat_b'
FIFO_READ = '/tmp/chat_a'
USERNAME = 'Usuario B'

def recibir():
    with open(FIFO_READ, 'r') as fifo_in:
        while True:
            mensaje = fifo_in.readline().strip()
            if mensaje:
                print(mensaje)

def enviar():
    with open(FIFO_WRITE, 'w') as fifo_out:
        while True:
            texto = input()
            if texto == '/exit':
                print("Saliendo del chat...")
                os._exit(0)
            timestamp = datetime.now().strftime('%H:%M:%S')
            fifo_out.write(f"[{timestamp}] {USERNAME}: {texto}\n")
            fifo_out.flush()

if __name__ == '__main__':
    threading.Thread(target=recibir, daemon=True).start()
    enviar()
