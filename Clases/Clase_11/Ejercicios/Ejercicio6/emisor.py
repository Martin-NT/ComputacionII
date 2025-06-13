import os

fifo_path = "/tmp/mi_fifo"

def main():
    with open(fifo_path, 'w') as fifo:
        print("Escribiendo mensaje en el FIFO...")
        fifo.write("Hola desde el emisor!\n")
        fifo.flush()  # Asegura que el mensaje se envía inmediatamente

if __name__ == "__main__":
    main()
