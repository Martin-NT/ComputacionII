# Ejercicio 5 · Nivel Experto

> **Objetivo**: diseñar un pipeline productor–consumidor usando `Pipe` doble.
s
> **Enunciado**: crea dos procesos hijos: `productor` genera 10 números pseudo‑aleatorios y los envía al padre; el padre los reenvía a un `consumidor`, que imprime el cuadrado de cada número. Implementa el pipeline con dos `Pipe()`, asegurando el cierre limpio de extremos y detectando fin de datos mediante envío del valor `None`.

- **Comentario**: se manejan dos pipes independientes y señal de terminación.