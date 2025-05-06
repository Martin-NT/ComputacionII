import os

fifo_path = '/tmp/test_fifo'
with open(fifo_path, 'r') as fifo:
    print("Esperando datos...")
    data = fifo.read()
    print(f"Recibido: {data}")
