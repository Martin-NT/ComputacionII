### Ejercicio 6 — Chat asincrónico con doble FIFO
**Objetivo**: Crear una estructura de comunicación bidireccional entre dos usuarios.

**Instrucciones**:
1. Crear dos FIFOs: `/tmp/chat_a` y `/tmp/chat_b`.
2. Usuario A escribe en `chat_a` y lee de `chat_b`, y viceversa.
3. Implementar dos scripts simétricos, uno para cada usuario.

**Extras**:
- Permitir comandos como `/exit` para salir.
- Mostrar los mensajes con nombre de emisor y timestamp.

---

### Ejecución

- Crear los Fifos
mkfifo /tmp/chat_a
mkfifo /tmp/chat_b

- En una terminal:
python3 usuario_a.py

- En otra terminal:
python3 usuario_b.py

Ahora podrás chatear entre terminales de forma bidireccional. Para salir, escribí /exit.