# 📚 Guía de Estudio - Pipes en Programación Concurrente (Computación II)

## 1. 🧠 Fundamentos teóricos de Pipes

### ¿Qué es un pipe?
Un **pipe** es un mecanismo de comunicación entre procesos (IPC) que permite que los datos **fluyan en una sola dirección** de un proceso a otro, como una tubería.

### Características:
- Unidireccional (por defecto).
- Transfiere datos en forma de bytes.
- Se cierra explícitamente.
- Está **vivo mientras los procesos estén activos** (pipe sin nombre).
- **Pipe con nombre (named pipe/FIFO)**: persiste en el sistema de archivos.

### ¿Por qué son importantes?
Permiten separar responsabilidades: un proceso produce datos, otro los consume. Se usan en sistemas operativos y programación concurrente para **dividir el trabajo entre procesos**.

---

## 2. ⚙️ Implementación interna y ciclo de vida

- Se crean usando `os.pipe()` o `multiprocessing.Pipe()` en Python.
- El sistema devuelve dos **file descriptors**:
  - Uno para lectura.
  - Uno para escritura.

### Ciclo de vida:
1. Se crea el pipe.
2. Se pasa uno o ambos extremos a procesos hijos.
3. Se comunican usando `.send()` / `.recv()` o `.write()` / `.read()`.
4. Se cierran los extremos cuando no se usan más.

---

## 3. 🛠️ Implementación básica en Python

### Usando `multiprocessing.Pipe`:

```python
from multiprocessing import Pipe, Process

def child_process(conn):
    mensaje = conn.recv()
    print("Hijo recibió:", mensaje)
    conn.send("Hola padre!")
    conn.close()

if __name__ == "__main__":
    padre_conn, hijo_conn = Pipe()
    p = Process(target=child_process, args=(hijo_conn,))
    p.start()
    padre_conn.send("Hola hijo")
    respuesta = padre_conn.recv()
    print("Padre recibió:", respuesta)
    p.join()
```

---

## 4. 🔄 Comunicación unidireccional

### Ejemplo simple:
Un proceso envía un mensaje, el otro lo recibe.

#### Resumen del flujo:
1. El padre envía un mensaje al hijo.
2. El hijo lo recibe y responde.
3. El padre recibe la respuesta.

---

## 5. 📦 Patrones avanzados

### 📍 Pipeline (cadena de procesos)

```python
from multiprocessing import Pipe, Process

def productor(conn):
    conn.send(10)
    conn.close()

def procesador(conn_in, conn_out):
    numero = conn_in.recv()
    conn_out.send(numero * 2)
    conn_in.close()
    conn_out.close()

def consumidor(conn):
    print("Resultado final:", conn.recv())
    conn.close()

if __name__ == "__main__":
    p1_conn_out, p1_conn_in = Pipe()
    p2_conn_out, p2_conn_in = Pipe()

    p1 = Process(target=productor, args=(p1_conn_in,))
    p2 = Process(target=procesador, args=(p1_conn_out, p2_conn_in))
    p3 = Process(target=consumidor, args=(p2_conn_out,))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
```

---

### 🔁 Comunicación Bidireccional

```python
from multiprocessing import Pipe, Process

def hijo(conn):
    mensaje = conn.recv()
    print("Hijo recibió:", mensaje)
    conn.send(f"Recibido: {mensaje}")
    conn.close()

if __name__ == "__main__":
    padre_conn, hijo_conn = Pipe()
    p = Process(target=hijo, args=(hijo_conn,))
    p.start()
    padre_conn.send("Hola hijo, ¿me escuchás?")
    print("Padre recibió respuesta:", padre_conn.recv())
    p.join()
```

---

## 6. 🛡️ Prevención de errores y deadlocks

### Problemas comunes:
- Deadlocks: procesos esperando datos que nunca llegan.
- Fugas de recursos: no cerrar pipes.
- Bloqueo en `.recv()` si no se envían datos.

### Estrategias:
1. **Cerrar extremos no usados**:
   ```python
   conn.close()
   ```
2. **Orden correcto de `.send()` y `.recv()`**:
   - Primero se envía, luego se recibe.
3. **Uso de `poll()`**:
   ```python
   if conn.poll(5):
       data = conn.recv()
   ```
4. **Diseñar procesos simples** y con una responsabilidad clara.

---

## 📌 Preguntas de comprensión con respuestas

### Sección 1 (teoría):
1. ¿Cuál es la diferencia entre pipe sin nombre y pipe con nombre?  
   → El pipe sin nombre vive mientras los procesos están en ejecución; el pipe con nombre persiste más tiempo.

2. ¿Por qué se llaman pipes?  
   → Porque los datos **fluyen en una sola dirección**, como en una tubería.

3. ¿Quién gestiona el acceso concurrente al pipe?  
   → El sistema operativo.

---

### Sección 3 (implementación):
1. ¿Qué devuelve `Pipe()`?  
   → Dos objetos `Connection`: uno para leer, otro para escribir.

2. ¿Por qué hay que cerrar los extremos no usados?  
   → Para evitar errores y liberar recursos.

3. ¿Qué pasa si cerramos un pipe antes de `fork()` o `Process()`?  
   → Ya no se pueden usar los extremos desde el nuevo proceso.

---

### Sección 5 (pipeline y bidireccional):
1. ¿Qué parámetro hace que un pipe sea bidireccional?  
   → `duplex=True` (es el valor por defecto).

2. ¿Cómo se comunican los procesos en comunicación bidireccional?  
   → Ambos usan `.send()` y `.recv()` en el mismo pipe.

3. ¿Qué pasa si ambos hacen `.recv()` primero?  
   → Se produce un **deadlock** porque ambos quedan esperando.

---

### Sección 6 (errores comunes):
1. ¿Qué hace `conn.poll()`?  
   → Revisa si hay datos antes de hacer `.recv()`, evitando bloqueos.

2. ¿Por qué es importante cerrar los extremos del pipe?  
   → Para evitar deadlocks y fugas de recursos.

3. ¿Qué causa un deadlock?  
   → Dos procesos esperando datos que el otro no envía.

---

## ✅ Buenas prácticas

- Usar nombres descriptivos (`padre_conn`, `hijo_conn`).
- Cerrar conexiones cuando ya no se usan.
- Documentar procesos con comentarios.
- Probar paso a paso usando `print()`.
- Compartir avances con el profesor periódicamente.

---

## 🧾 Créditos y mantenimiento

Autor: ChatGPT + [Tu Nombre]  
Fecha: Abril 2025  
Descripción: Guía teórico-práctica sobre pipes en programación concurrente usando Python.

---

## 🔹 1. ¿Qué son los Pipes? – Fundamentos Conceptuales

### 📘 Definición
Un pipe (tubería) es un mecanismo de comunicación que permite que dos procesos intercambien datos de manera unidireccional, es decir, uno escribe y el otro lee. Fue introducido en los sistemas Unix y es uno de los mecanismos más antiguos y eficientes para la comunicación entre procesos (IPC, Inter-Process Communication).

### 📌 Importancia en Sistemas Operativos
- Los pipes permiten que procesos colaboren sin compartir memoria.
- Fomentan la modularidad (cada proceso puede hacer una parte del trabajo).
- Son fundamentales en sistemas Unix/Linux, por ejemplo en la terminal:
```bash
ls | grep ".txt"
```
Acá, el resultado de `ls` (proceso A) se pasa a `grep` (proceso B) mediante un pipe.

### 🚦 Características clave
- **Unidireccionales**: datos fluyen en una sola dirección.
- **Anónimos o con nombre**:
  - *Anónimos*: existen solo mientras los procesos estén en ejecución.
  - *Con nombre (FIFOs)*: tienen un nombre en el sistema de archivos y sobreviven más tiempo.
- **Buffer limitados**: si el buffer del pipe se llena, el proceso escritor se bloquea hasta que el lector libere espacio.
- **Sincronización implícita**: el pipe fuerza a que los procesos colaboren al ritmo del otro.

### 🧠 Preguntas de comprensión
- ¿Cuál es la diferencia principal entre un pipe anónimo y uno con nombre?
  - ✅ El anónimo existe mientras los procesos viven; el FIFO tiene un nombre y persiste más.
- ¿Por qué decimos que los pipes son unidireccionales?
  - ✅ Porque los datos fluyen en una sola dirección: uno escribe, otro lee.
- ¿Qué sucede si el proceso lector no consume los datos del pipe?
  - ✅ El escritor se bloquea porque el buffer se llena.

---

## 🔹 2. Implementación Interna y Ciclo de Vida de un Pipe

### ⚙️ ¿Cómo funciona un pipe internamente en el sistema operativo?
- Es una estructura del kernel que actúa como buffer circular.
- El SO administra acceso concurrente seguro.

### 📋 Etapas del ciclo de vida
1. **Creación**: `os.pipe()` devuelve dos file descriptors.
2. **Uso**: uno escribe, otro lee. Si no hay datos o espacio, se bloquea.
3. **Herencia**: se pueden compartir extremos con `fork()` o `multiprocessing`.
4. **Cierre**: se deben cerrar los extremos. El SO libera el buffer al final.

### 📌 Analogía visual
Imaginá un tubo con cartas: si no se sacan, no se pueden meter más.

### 🧠 Preguntas de comprensión
- ¿Qué devuelve el sistema cuando se crea un pipe?
  - ✅ Dos file descriptors: uno para leer y otro para escribir.
- ¿Por qué es importante cerrar los extremos del pipe que no se usan?
  - ✅ Para evitar errores y bloqueos.
- ¿Qué pasa si nadie cierra un extremo del pipe después de usarlo?
  - ✅ El SO no libera el recurso, y pueden ocurrir fugas.

---

## 🔹 3. Implementar Pipes en Python con os.pipe()

### 📦 Módulos necesarios
```python
import os
import multiprocessing
```

### ✅ ¿Qué hace `os.pipe()`?
Devuelve dos file descriptors: uno para lectura (r) y otro para escritura (w).

### 🧪 Ejemplo práctico: hijo escribe y padre lee
(ver ejemplo en sección previa del archivo)

### 🧠 Preguntas de comprensión
- ¿Qué función usamos para escribir datos en el pipe?
  - ✅ `os.write()`
- ¿Por qué cerramos `r` en el hijo y `w` en el padre?
  - ✅ Para evitar bloqueos y garantizar la comunicación correcta.
- ¿Qué tipo de datos deben escribirse en el pipe?
  - ✅ Bytes (`b"mensaje"`), no texto directamente.

---

## 🔹 4. Comunicación entre procesos con `multiprocessing.Pipe()`

### 📘 ¿Qué es?
Una abstracción que permite comunicación entre procesos con objetos `Connection`.

### ✅ ¿Qué devuelve?
Dos objetos: ambos pueden enviar y recibir. Pero se recomienda usar uno para cada tarea.

### 🧪 Ejemplo práctico
(ver ejemplo en sección previa del archivo)

### 🧠 Preguntas de comprensión
- ¿Qué método usamos para enviar datos por el pipe?
  - ✅ `.send()`
- ¿Qué ventajas ofrece `multiprocessing.Pipe()` frente a `os.pipe()`?
  - ✅ Más simple, legible, y admite tipos de datos Python.
- ¿Cuál es el paso clave luego de enviar o recibir?
  - ✅ `.close()` la conexión.

---

## 🔹 5. Patrones avanzados: Pipeline y Comunicación Bidireccional

### Ejemplo 1: Pipeline
Tres procesos: Productor → Procesador → Consumidor.
(ver ejemplo en archivo)

### 🧠 Preguntas de comprensión
- ¿Qué pasa si no cerramos los pipes al final?
  - ✅ Pueden quedar procesos colgados o recursos no liberados.
- ¿Cómo se llama este patrón?
  - ✅ Pipeline.
- ¿Qué tarea cumple el procesador?
  - ✅ Transforma el dato recibido.

### Ejemplo 2: Comunicación Bidireccional
Usamos `Pipe(duplex=True)` para enviar y recibir en ambos extremos.

### 🧠 Preguntas de comprensión
- ¿Qué parámetro permite que un pipe sea bidireccional?
  - ✅ `duplex=True`.
- ¿Cómo se comunican ambos procesos?
  - ✅ Usan `.send()` y `.recv()` en ambos extremos.
- ¿Qué pasa si ambos hacen `.recv()` primero?
  - ✅ Ambos quedan bloqueados esperando datos.

---

## 🔹 6. Estrategias para prevenir problemas comunes con Pipes

### 🧱 Problemas comunes
- Deadlocks
- Fugas de recursos
- Bloqueos por falta de datos

### 🛡️ Estrategias
1. **Cerrar extremos no usados**
2. **Orden correcto de operaciones**
3. **Usar `poll()` con timeout**
4. **No reutilizar pipes cerrados**
5. **Diseñar procesos simples**

### 🎓 Buenas prácticas
- Nombres descriptivos
- Cerrar todo al final
- Agregar prints para debugging
- Documentar

### 🧠 Preguntas de comprensión
- ¿Qué hace `conn.poll()`?
  - ✅ Verifica si hay datos antes de hacer `.recv()`.
- ¿Por qué es importante cerrar los extremos?
  - ✅ Para evitar fugas y bloqueos.
- ¿Qué puede causar un deadlock?
  - ✅ Esperar datos de un proceso que nunca los envía.
