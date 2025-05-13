# Ejercicio 1 · Nivel Básico

> **Objetivo**: comprobar la creación de procesos y la correcta espera del padre.

> **Enunciado**: escribe un programa que cree dos procesos hijo mediante `multiprocessing.Process`, cada uno imprimiendo su propio `pid`. El proceso padre debe esperar a que ambos terminen y luego imprimir un mensaje de cierre.

- **Comentario**: se ilustra el ciclo `start() → join()` y la diferenciación de PIDs.