#📌 Objetivo: Crear un hijo que termine inmediatamente y un padre que no llame wait().

import os
import time

pid = os.fork()

if pid == 0:  
    print(f"Soy el proceso hijo {os.getpid()} y voy a terminar.")
    exit(0)  # Hijo termina inmediatamente
else:  
    print(f"Soy el padre {os.getpid()}, pero no llamaré wait().")
    time.sleep(10)  # El padre sigue vivo sin limpiar al hijo
    print("Padre finalizando.")

#📌 Ejecuta en otra terminal mientras el padre sigue vivo:
#   ps aux | grep Z

#✅ Solución: Si agregas os.wait(), el zombi desaparece.