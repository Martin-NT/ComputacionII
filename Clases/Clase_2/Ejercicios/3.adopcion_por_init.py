#📌 Objetivo: Ver cómo un hijo huérfano cambia su PPID a 1.

import os
import time

pid = os.fork()

if pid == 0:  # Código del hijo
    print(f"Hijo {os.getpid()} iniciado, mi padre es {os.getppid()}")
    time.sleep(5)  # Dormir mientras el padre termina
    print(f"Ahora mi padre es {os.getppid()} (debería ser 1 si fui adoptado por init).")
else:
    print(f"Padre {os.getpid()} terminando antes que su hijo.")
    exit(0)  # El padre termina inmediatamente

#🔍 ¿Qué observar?
#   Cuando el padre termina, el hijo cambia su PPID a 1 (init lo adopta).

#🔎 ¿Por qué el PPID del huérfano no siempre es 1?

#-En algunos sistemas modernos (como Ubuntu con systemd), no siempre es 1 (init) quien adopta los 
# procesos huérfanos.

#-Puede ser otro proceso del sistema, como systemd, que maneja procesos en lugar de init.

#-Por eso viste 1696 en lugar de 1, porque systemd (o un proceso intermedio) adoptó al hijo.

#✅ Prueba esto:
#   Ejecuta el comando en la terminal: ps -fp 1634
#🔍 Esto te dirá qué proceso adoptó al hijo.