with open('/tmp/temp_fifo', 'r') as fifo:
    while True:
        temp = int(fifo.readline().strip())
        print(f"Temperatura: {temp}°C")
        if temp > 28:
            print("¡ALERTA! Temperatura alta")
