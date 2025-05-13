# Ejercicio 2 · Nivel Intermedio

> **Objetivo**: usar `Queue` para reunir resultados de varios procesos.

> **Enunciado**: implementa un script que genere $n = 4$ procesos; cada proceso calcula la suma de los primeros $k = 1\,000\,000$ enteros y deposita el resultado en una `Queue`. El padre recoge los cuatro resultados y verifica que sean idénticos.

- **Comentario**: se observa comunicación **many‑to‑one** y verificación de integridad.