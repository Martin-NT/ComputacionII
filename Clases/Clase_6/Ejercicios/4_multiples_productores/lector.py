with open('/tmp/fifo_multi', 'r') as fifo:
    while True:
        print(fifo.readline(), end="")
