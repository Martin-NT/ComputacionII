import os
import threading

def recibir():
    with open('/tmp/chat_b_a', 'r') as fifo_in:
        while True:
            msg = fifo_in.readline()
            if msg:
                print(f"[B]: {msg.strip()}")

def enviar():
    with open('/tmp/chat_a_b', 'w') as fifo_out:
        while True:
            msg = input("[A]: ")
            fifo_out.write(msg + '\n')
            fifo_out.flush()

# Hilo para recibir mensajes
threading.Thread(target=recibir, daemon=True).start()
enviar()
