
# Resumen: Uso de FIFOs en Unix/Linux

## 1. Fundamentos de FIFOs

- **FIFO (First-In-First-Out)** es un mecanismo de comunicación entre procesos en Unix/Linux.
- A diferencia de los *pipes* anónimos, los **FIFOs son archivos especiales** ubicados en el sistema de archivos, lo que permite la comunicación entre procesos no relacionados.
- Los datos en un FIFO son leídos en el orden en que se escribieron, garantizando el comportamiento FIFO.

## 2. Conceptos Importantes

### 2.1 Creación de un FIFO

Para crear un FIFO, se utiliza el comando `mkfifo`:

```bash
$ mkfifo /tmp/mi_fifo
```

Esto genera un archivo especial que puede ser abierto por varios procesos para comunicación.

### 2.2 Lectura y Escritura en un FIFO

Los FIFOs se manejan a través de las llamadas al sistema `open()`, `read()`, y `write()`. Ejemplo básico:

#### Escritura en FIFO:
```python
import os

fd = os.open('/tmp/mi_fifo', os.O_WRONLY)
os.write(fd, b'Hola desde os.write
')
os.close(fd)
```

#### Lectura de FIFO:
```python
import os

fd = os.open('/tmp/mi_fifo', os.O_RDONLY)
data = os.read(fd, 1024)
print('Lectura:', data.decode())
os.close(fd)
```

### 2.3 Bloqueo y `O_NONBLOCK`

El uso de la bandera `O_NONBLOCK` evita que el proceso se bloquee si no hay datos disponibles para leer:

```python
fd = os.open('/tmp/mi_fifo', os.O_RDONLY | os.O_NONBLOCK)
```

Esto permite continuar con otras tareas si no hay datos disponibles.

### 2.4 Comportamiento del Cursor

Los datos leídos de un FIFO **no pueden ser leídos de nuevo** por otro proceso. El primer proceso que lea consume esos datos.

## 3. Ejercicios Prácticos

### 3.1 Chat entre dos procesos

Se crea un sistema de chat donde dos procesos se comunican a través de dos FIFOs.

#### Ejemplo:

- **Proceso 1 (escribe)**:
```python
# escritor.py
with open('/tmp/fifo_in', 'w') as fifo:
    fifo.write("Hola, ¿cómo estás?")
```

- **Proceso 2 (lee y responde)**:
```python
# lector.py
with open('/tmp/fifo_in', 'r') as fifo:
    mensaje = fifo.readline()
    print(f"Mensaje recibido: {mensaje}")
```

### 3.2 Log en tiempo real con FIFO

Se implementa un sistema de logging donde los mensajes de log se escriben en un FIFO y son leídos por un proceso lector.

#### Ejemplo de log:

- **Escritor de log**:
```python
# logger.py
with open('/tmp/log_fifo', 'w') as fifo:
    fifo.write("Este es un mensaje de log.
")
```

- **Lector de log**:
```python
# lector_log.py
with open('/tmp/log_fifo', 'r') as fifo:
    log = fifo.readline()
    print(f"Log leído: {log}")
```

### 3.3 Multiplexado de múltiples FIFOs con `select.select()`

Se utiliza `select.select()` para manejar múltiples FIFOs sin bloqueos, ideal para sistemas donde múltiples fuentes de datos están involucradas.

#### Ejemplo:
```python
import select
import os

fifo_1 = os.open('/tmp/fifo_1', os.O_RDONLY)
fifo_2 = os.open('/tmp/fifo_2', os.O_RDONLY)

while True:
    readable, _, _ = select.select([fifo_1, fifo_2], [], [])
    for fd in readable:
        print(os.read(fd, 1024).decode())
```

## 4. Preguntas de Comprensión

- ¿Por qué usamos un FIFO por cada dirección de comunicación en un chat?
- ¿Qué ventaja tiene usar hilos (threads) en el ejercicio de múltiples procesos?
- ¿Qué pasa si uno de los procesos termina abruptamente en un sistema de FIFO?

## 5. Consideraciones Adicionales

- **Sincronización**: Los FIFOs gestionan de manera interna la sincronización entre los procesos productores y consumidores.
- **Permisos**: Asegúrate de que los permisos del FIFO sean adecuados para evitar accesos no autorizados.

## 6. Conclusión

Los **FIFOs** son herramientas potentes y sencillas para la **comunicación entre procesos** en sistemas Unix/Linux. Permiten que procesos no relacionados se comuniquen de manera eficiente, garantizando el orden de llegada de los datos.

---

**Recuerda** practicar los ejemplos, realizar los ejercicios propuestos y experimentar con diferentes configuraciones de lectura y escritura para entender mejor su funcionamiento.
