# Ejercicio 1: Manejo básico con `SIGTERM`

**Objetivo:** Familiarizarse con el uso de `SIGTERM` y funciones de limpieza al finalizar un proceso.

**Enunciado:**
Crea un programa que capture la señal `SIGTERM` y, en respuesta, muestre un mensaje de despedida. Asegúrate de registrar una función con `atexit` para que se ejecute al terminar el proceso, independientemente del motivo de finalización.

---

## Probarlo

1. Corre el programa en una terminal.
2. Desde otra terminal, encuentra el PID del proceso con ps aux | grep python.
3. Envía la señal con kill -SIGTERM <PID>.

Esto debería imprimir "Señal SIGTERM recibida." y luego "El proceso ha terminado correctamente".