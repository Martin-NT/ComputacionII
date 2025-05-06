### Ejercicio 5 — FIFO con apertura condicional
**Objetivo**: Usar `os.open()` y manejar errores.

**Instrucciones**:
1. Usar `os.open()` con flags como `O_NONBLOCK`.
2. Crear un lector que intente abrir el FIFO sin bloquear.
3. Si el FIFO no tiene escritores, debe imprimir un mensaje y salir correctamente.

**Desafío adicional**: Hacer que el lector reintente 5 veces con espera entre intentos antes de salir.

---

### Ejecución

- Crear FIFO: mkfifo /tmp/fifo_condicional
- Ejecutar el lector en una terminal.

