import os

fifo_path = "/tmp/mi_fifo"

def main():
    print("Esperando mensaje en el FIFO...")
    with open(fifo_path, 'r') as fifo:
        for linea in fifo:
            print("--> Mensaje recibido:", linea.strip())

if __name__ == "__main__":
    main()
