# Ejercicio 2: Diferenciar señales según su origen

**Objetivo:** Comprender cómo múltiples señales pueden ser diferenciadas en un mismo handler.

**Enunciado:**
El proceso principal debe lanzar tres procesos hijos. Cada hijo, luego de un pequeño retardo aleatorio, debe enviar una señal distinta al padre (`SIGUSR1`, `SIGUSR2`, `SIGTERM`). El padre debe manejar todas las señales con un solo handler y registrar cuál hijo envió qué señal, usando `os.getpid()` y `os.getppid()`.

---

## Probarlo

1. Ejecuta el programa.
2. Observa cómo el padre recibe las señales de los hijos con sus respectivos pid.