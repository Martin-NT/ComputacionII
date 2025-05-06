import os

fifo_path = '/tmp/log_fifo'
with open(fifo_path, 'r') as fifo, open('output.txt', 'a') as log_file:
    while True:
        data = fifo.readline()
        if data.strip() == "exit":
            break
        log_file.write(data)
        log_file.flush()
