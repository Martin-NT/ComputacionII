import os
import time

pid = os.fork()

if pid == 0:  # Proceso hijo
    print(f"Soy el proceso hijo (PID {os.getpid()}), mi padre es {os.getppid()}")
    time.sleep(5)  # Dormimos para asegurarnos de que el padre termine primero
    print(f"Ahora mi padre es {os.getppid()} (debería ser 1 si fui adoptado por init).")
else:  # Proceso padre
    print(f"Soy el padre (PID {os.getpid()}), voy a terminar antes que mi hijo.")
    exit(0)  # El padre termina inmediatamente

#🔍 ¿Cómo ocurre un proceso huérfano?
#   El proceso padre finaliza antes que su hijo.
#   El sistema operativo reasigna el hijo a init (PID = 1) para que lo adopte.

#🔍 ¿Qué esperar?
#   El padre finaliza antes que el hijo.
#El sistema operativo cambia el PPID del hijo a 1 (init lo adopta).

#✅ Solución:
#   No es un problema grave porque init se encarga de los huérfanos.
#   Buena práctica: Asegurarse de que el padre no termine antes del hijo si es importante para 
#   la lógica del programa.