import os
import time

pid = os.fork()

if pid == 0:  # Proceso hijo
    print("Soy el proceso hijo y voy a terminar inmediatamente.")
    exit(0)  # Termina el proceso hijo
    
else:  # Proceso padre
    print(f"Soy el padre, mi hijo tiene PID {pid}. No llamaré wait()...")
    time.sleep(10)  # El padre no recoge el estado del hijo
    print("Padre terminando.")

#🔍 ¿Cómo ocurre un proceso zombi?
#   El proceso hijo finaliza.
#   Su información sigue en la tabla de procesos hasta que el padre llame a wait().
#   Si el padre nunca llama a wait(), el proceso queda como un zombi.

#🔍 ¿Qué esperar?
#   El hijo termina enseguida.
#   El padre sigue vivo por 10 segundos sin llamar a wait().
#   Durante ese tiempo, el hijo aparece como zombi (Z+) en la lista de procesos.

#📌 Para ver el zombi, ejecuta en otra terminal:
#   ps aux | grep Z

#✅ Solución:
#   Llamar a wait() en el padre para eliminar la entrada del hijo de la tabla de procesos.