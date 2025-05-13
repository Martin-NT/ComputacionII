#### Ejercicio 7 · Nivel Intermedio +

Desarrolla un *load balancer* simple: un proceso maestro reparte una lista de URLs a descargar entre `k` procesos *worker* mediante una `Queue`. Cada *worker* registra su PID y el tiempo de descarga. Al finalizar, el maestro debe generar un reporte ordenado por duración.