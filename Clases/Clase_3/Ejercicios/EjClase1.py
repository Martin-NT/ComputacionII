import os
import time 

def crear_hijo(wait_time, message):
    pid = os.fork()
    if pid == 0:
        time.sleep(wait_time) #tarea minima
        print(f"--> {message}, mi PID es {os.getpid()} y el PID de mi padre es {os.getppid()}")
        os._exit(0)

if __name__ == "__main__":
    crear_hijo(2, "Soy el Hijo 1")
    crear_hijo(4, "Soy el Hijo 2")
    
    #time.sleep(1)
    os.waitpid(-1, 0)
        # -1 indica que puede esperar a cualquier hijo.
        # 0 hace que waitpid() se bloquee hasta que un hijo termine.
    print(f"--> Soy el Padre, mi PID es {os.getpid()}")
    