### Ejercicio 3 — FIFO + archivos
**Objetivo**: Usar un FIFO como entrada para un proceso que guarda datos en un archivo.

**Instrucciones**:
1. Crear un script que escuche un FIFO y guarde todo lo que llega en `output.txt`.
2. Otro script debe leer líneas desde el teclado y enviarlas al FIFO.
3. Al escribir "exit" se debe cerrar todo correctamente.

---

### Ejecución:

- Crear FIFO: mkfifo /tmp/log_fifo
- Ejecutar el escucha_fifo: python3 escucha_fifo.py
- Ejecutar el escribir_fifo: python3 escribir_fifo.py