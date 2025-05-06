import os
import threading

def recibir():
    with open('/tmp/chat_a_b', 'r') as fifo_in:
        while True:
            msg = fifo_in.readline()
            if msg:
                print(f"[A]: {msg.strip()}")

def enviar():
    with open('/tmp/chat_b_a', 'w') as fifo_out:
        while True:
            msg = input("[B]: ")
            fifo_out.write(msg + '\n')
            fifo_out.flush()

threading.Thread(target=recibir, daemon=True).start()
enviar()
