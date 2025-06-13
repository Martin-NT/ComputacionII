import os
import sys

def main():
    print(f"Proceso padre PID: {os.getpid()}")

    pid = os.fork()  # Crea un proceso hijo

    if pid == 0:
        # Este bloque se ejecuta SOLO en el proceso hijo
        print(f"Hijo creado con PID: {os.getpid()} - reemplazando imagen con 'sh -c \"ls -l; sleep 5\"'")
        
        # Reemplaza el hijo con el comando: "ls -l" y luego "sleep 5"
        os.execvp("sh", ["sh", "-c", "ls -l; sleep 5"])

        # Si exec falla (lo cual no debería), imprime error y sale
        print("Error: execvp falló")
        sys.exit(1)

    else:
        # Este bloque lo ejecuta solo el padre
        print("Padre esperando a que el hijo termine...")
        os.wait()  # Espera a que el hijo termine
        print("Hijo terminó, padre también termina.")

if __name__ == "__main__":
    main()
