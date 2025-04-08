"""Ejercicio 6: Proceso huérfano adoptado por `init`"""
# Genera un proceso hijo que siga ejecutándose luego de que el padre haya terminado. 
# Verifica que su nuevo PPID corresponda al proceso `init` o `systemd`.

import os
import time

# Creación de un proceso hijo mediante fork
pid = os.fork()

if pid > 0:  # Código que ejecuta el proceso padre
    # El proceso padre imprime que va a terminar
    print("[PADRE] --> Soy el proceso padre, mi PID es:", os.getpid())
    print("[PADRE] --> Mi ejecución está terminando, lo que deja al proceso hijo huérfano.")
    print("----------------------------------------------------------------------------------------------")
    
    # El padre termina su ejecución, dejando al proceso hijo huérfano
    os._exit(0)

else:  # Código que ejecuta el proceso hijo
    print("[HIJO] --> Soy el proceso hijo, mi PID es:", os.getpid())
    print("[HIJO] --> Mi proceso padre ha terminado, por lo que ahora soy huérfano.")
    print("----------------------------------------------------------------------------------------------")
    
    # El hijo duerme 30 segundos para permitir la observación del cambio en el PPID
    print("[HIJO] --> Mi nuevo padre será el proceso 'init' o 'systemd', que tiene PID 1.")
    print(f"[HIJO] --> Revisa el proceso huérfano con el siguiente comando en otra terminal:")
    print(f"    ps -o pid,ppid,comm -p {os.getpid()}")
    time.sleep(30)  # El hijo duerme 30 segundos para que podamos verificar el PPID

    # Después de dormir, el hijo imprime su nuevo PPID (debe ser 1)
    print("----------------------------------------------------------------------------------------------")
    print("[HIJO] --> Mi PPID ahora es:", os.getppid())  # El nuevo PPID debe ser 1
    print("[HIJO] --> Ahora termino mi ejecución.")

