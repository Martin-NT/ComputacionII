# Ejercicio 3 · Nivel Intermedio +

> **Objetivo**: demostrar una condición de carrera y su corrección con `Lock`.
>
> **Enunciado**: crea un contador global al que dos procesos suman 1, cincuenta mil veces cada uno. Realiza primero la versión sin `Lock` (para evidenciar valores erróneos) y luego protégela con un `Lock`, mostrando el resultado correcto (`100 000`).

- **Comentario**: `Value` permite memoria compartida; el `Lock` garantiza atomicidad.
