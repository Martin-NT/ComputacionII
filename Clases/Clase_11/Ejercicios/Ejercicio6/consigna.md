## Ejercicio 6: FIFO (named pipe) entre dos scripts

Cree un FIFO en `/tmp/mi_fifo` usando Bash (`mkfifo`). Luego:

- Escriba un script `emisor.py` que escriba mensajes en el FIFO.
- Escriba un script `receptor.py` que lea desde el FIFO e imprima los mensajes.

Ejecute ambos scripts en terminales distintas.

---

## 🧠 ¿Qué es un FIFO (named pipe)?
- Un FIFO es un archivo especial que actúa como un canal de comunicación entre procesos.
- Se comporta como un pipe, pero tiene un nombre y ruta en el sistema de archivos.
- Se crea con mkfifo y se usa como si fuera un archivo de texto.

## Pasos para Ejecutar
### 🛠 Paso 1: Crear el FIFO
Abrí una terminal y ejecutá:
```bash
mkfifo /tmp/mi_fifo
```
Esto crea un archivo especial en /tmp/mi_fifo.
### En una terminal ejecuta
Terminal 1 – receptor
```bash
python3 receptor.py
```
Esto queda esperando que alguien le escriba al FIFO.

### En otra terminal 
Terminal 2 – emisor
```bash
python3 emisor.py
```
Esto escribe un mensaje en el FIFO.

### Cuando termines, podés borrar el FIFO con:
```bash
rm /tmp/mi_fifo
```