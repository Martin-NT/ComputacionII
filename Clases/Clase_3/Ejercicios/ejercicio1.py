"""Ejercicio 1: Identificación de procesos padre e hijo"""
# Crea un programa que genere un proceso hijo utilizando `fork()` y que ambos (padre e hijo) 
# impriman sus respectivos PID y PPID. El objetivo es observar la relación jerárquica entre ellos.

import os

pid = os.fork()

if pid == 0:
    print("--> [Proceso Hijo] PID:", os.getpid(), "- PPID:", os.getppid())
else:
    print("--> [Proceso Padre] PID:", os.getpid(), "- Hijo:", pid)