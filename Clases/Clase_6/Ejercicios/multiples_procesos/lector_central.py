# lector_central.py
fifo_path = "/tmp/multilog_fifo"

with open(fifo_path, "r") as fifo:
    print("🔁 Lector central esperando mensajes...")
    while True:
        line = fifo.readline()
        if line:
            print(f"[LOG] {line.strip()}")
