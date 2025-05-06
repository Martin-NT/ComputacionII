# logger1.py
import time

with open("/tmp/multilog_fifo", "w") as fifo:
    for i in range(5):
        msg = f"Logger 1 - Mensaje {i}\n"
        fifo.write(msg)
        fifo.flush()
        time.sleep(1)
