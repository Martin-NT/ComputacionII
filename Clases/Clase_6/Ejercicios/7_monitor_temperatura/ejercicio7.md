### Ejercicio 7 — Monitor de temperatura simulado
**Objetivo**: Simular un sensor que envía datos por FIFO y un visualizador que los muestra.

**Instrucciones**:
1. Script A (simulador): cada segundo escribe en el FIFO una temperatura aleatoria entre 20 y 30.
2. Script B (monitor): lee las temperaturas y muestra alertas si superan los 28 grados.

**Variante**: Agregar un log con fecha y hora.

---

### Ejecución

- Crear FIFO: mkfifo /tmp/temp_fifo
- Ejecutar el simulador y monitor en terminales separadas.