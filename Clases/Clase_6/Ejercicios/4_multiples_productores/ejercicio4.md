### Ejercicio 4 — Múltiples productores
**Objetivo**: Estudiar el comportamiento de múltiples escritores sobre un mismo FIFO.

**Instrucciones**:
1. Crear un FIFO `/tmp/fifo_multi`.
2. Ejecutar tres scripts distintos que escriban mensajes periódicamente (por ejemplo, "Soy productor 1", etc.).
3. Un solo lector debe mostrar los mensajes.

**Reflexión**: ¿Qué pasa si todos escriben al mismo tiempo? ¿Hay mezcla de líneas? ¿Es atómico?

---
### Ejecución

1. mkfifo /tmp/fifo_multi

2. Ejecutar los tres productores en tres terminales: 
python3 productor1.py
python3 productor2.py
python3 productor3.py

3. Ejecutar el lector en otra terminal: 
python3 lector.py

### Reflexión

Si todos los productores escriben al mismo tiempo, el lector puede ver mensajes entrecruzados. La escritura no es atómica en un FIFO estándar.