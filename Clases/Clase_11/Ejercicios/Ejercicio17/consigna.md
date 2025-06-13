## Ejercicio 17: Simulación de Lector y Escritor con FIFO

Cree dos scripts Bash: uno que escriba cada segundo en una FIFO y otro que lea continuamente. Analice qué sucede si el lector se lanza antes que el escritor y viceversa.

---

## 🧪 ¿Cómo probarlo?
1. Crear la FIFO:
```bash
mkfifo /tmp/mi_fifo
```
### Caso 1: Lector primero
2. En la terminal 1, lanza el lector:
```bash
bash lector.sh
```

3. En la terminal 2, lanza al escritor:
```bash
bash escritor.sh
```
🔁 Vas a ver cómo el lector muestra cada segundo un mensaje nuevo.
- El lector espera en silencio hasta que el escritor comience.
- En cuanto el escritor escriba, el lector empieza a mostrar mensajes.

### Caso 2: Escritor primero
2. En la terminal 1, lanza el escritor:
```bash
bash escritor.sh
```

3. En la terminal 2, lanza al lector:
```bash
bash lector.sh
```
- El escritor se bloquea en la línea echo > /tmp/mi_fifo hasta que haya un lector.
- En cuanto ejecutás el lector, se destraba y todo empieza a fluir.

4. Opcional: Para eliminar el fifo:
```bash
rm /tmp/mi_fifo
```

## Explicación 
Se implementó una comunicación tipo productor-consumidor usando una FIFO (/tmp/mi_fifo). El proceso escritor envía un mensaje por segundo y el lector lo recibe en tiempo real. Se observó que:
    - Si el lector inicia antes, espera silenciosamente hasta recibir datos.
    - Si el escritor inicia primero, se bloquea hasta que el lector esté listo.

Esto demuestra el comportamiento de sincronización natural de las FIFO en Bash: la escritura se suspende si no hay lectores, y la lectura bloquea si no hay datos disponibles.