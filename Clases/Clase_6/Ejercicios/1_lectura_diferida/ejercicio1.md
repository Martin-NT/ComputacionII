### Ejercicio 1 — Lectura diferida
**Objetivo**: Comprender el bloqueo de lectura en un FIFO.

**Instrucciones**:
1. Crear un FIFO llamado `/tmp/test_fifo`.
mkfifo /tmp/test_fifo

2. Ejecutar un script Python que intente leer desde el FIFO antes de que exista un escritor.
python3 lector.py

3. En otro terminal, ejecutar un script que escriba un mensaje en el FIFO.
python3 escritor.py

**Preguntas**:
1. ¿Qué se observa en el lector mientras espera?
El lector se bloquea hasta que el escritor ponga algo en el FIFO.

2. ¿Qué ocurre si se escriben múltiples líneas desde el escritor?
El lector leerá lo que haya en el FIFO en el momento en que intente leer. Si se escriben varias líneas, las leerá una vez que intente realizar la lectura.
---