
# Resumen Detallado - Procesos en Sistemas Operativos

## 1. **Fundamentos de los Procesos**
### Definición de Proceso
Un **proceso** es una instancia en ejecución de un programa. Es más que solo el código, incluye:
- **Estado** del proceso (en ejecución, suspendido, etc.).
- **Memoria** asignada al proceso.
- **Registros** del CPU para almacenar el estado de la ejecución.

### Diferencia entre Programa y Proceso
- **Programa:** Es un conjunto estático de instrucciones almacenadas en un archivo.
- **Proceso:** Es un programa en ejecución que tiene recursos como CPU, memoria y entradas/salidas asociadas a él.

### Atributos de un Proceso
- **PID (Process ID):** Identificador único asignado a cada proceso.
- **Estado:** El estado del proceso puede ser "en ejecución", "suspendido", "esperando", etc.
- **Memoria:** Cada proceso tiene su propia memoria, incluida la pila y el heap.

### Preguntas de comprensión:
1. **¿Qué diferencia a un proceso de un programa?**
   - Un **programa** es un conjunto de instrucciones estáticas, mientras que un **proceso** es una instancia en ejecución de ese programa.
   
2. **¿Qué es el PID de un proceso?**
   - El **PID** (Process Identifier) es un número único que el sistema operativo asigna a cada proceso para poder identificarlo.

---

## 2. **El Modelo de Procesos en UNIX/Linux**
### Jerarquía de Procesos
En los sistemas UNIX/Linux, todos los procesos están organizados jerárquicamente:
- Cada proceso tiene un **proceso padre** (excepto el proceso `init` o `systemd`, que tiene PID 1).
- Un **proceso padre** puede crear procesos hijos mediante `fork()`.

### El Proceso `init` o `systemd`
- El **proceso `init`** (o **`systemd`** en sistemas más modernos) es el primer proceso que arranca cuando se inicia el sistema, y todos los demás procesos derivan de él.
- Si un proceso hijo pierde su padre, **init** lo adopta.

### Herramientas para visualizar procesos
- Se puede usar **ps aux**, **pstree**, **htop** para ver todos los procesos y su jerarquía.

### Preguntas de comprensión:
1. **¿Qué es el proceso `init` y qué rol cumple?**
   - El **proceso `init`** (o `systemd`) es el proceso que arranca primero y actúa como el "padre" de todos los demás procesos.
   
2. **¿Cómo puedes visualizar la jerarquía de procesos?**
   - Se puede utilizar el comando `ps aux` para listar los procesos, o `pstree` para verlos en una estructura jerárquica.

---

## 3. **Creación y Manipulación de Procesos con Python**
### `fork()` y `exec()`
- **`fork()`**: Crea un nuevo proceso hijo que es una copia exacta del proceso padre. 
  - En el proceso hijo, `fork()` devuelve **0**.
  - En el proceso padre, devuelve el **PID del hijo**.
  
- **`exec()`**: Permite que un proceso hijo ejecute un nuevo programa, reemplazando su código original por el nuevo.

### Ejemplo de uso de `fork()` y `exec()`:
```python
import os

pid = os.fork()  # Crear un proceso hijo

if pid == 0:  # Código del hijo
    print("Soy el hijo")
else:  # Código del padre
    print("Soy el padre")
```

### Sincronización entre procesos
- **`wait()`**: Permite que el proceso padre espere a que el proceso hijo termine antes de continuar su ejecución.

### Preguntas de comprensión:
1. **¿Qué hace la función `fork()` en Python?**
   - `fork()` crea un proceso hijo, devolviendo **0** al hijo y el PID del hijo al padre.
   
2. **¿Para qué se utiliza `wait()`?**
   - `wait()` permite que el proceso padre espere a que sus procesos hijos terminen antes de continuar su ejecución.

---

## 4. **Procesos Zombis y Huérfanos**
### Procesos Zombis
Un **proceso zombi** es un proceso que ha terminado su ejecución, pero sigue siendo visible en la tabla de procesos hasta que el proceso padre llama a `wait()` para leer el código de salida del hijo.

- **Causas:** El padre no ha llamado a `wait()` para recoger el estado del hijo.
- **Consecuencias:** Los procesos zombis siguen ocupando espacio en la tabla de procesos.

### Procesos Huérfanos
Un **proceso huérfano** es un proceso cuyo padre ha terminado antes que él. En este caso, el proceso **init** (PID 1) lo adopta para que siga funcionando normalmente.

### Manejo de procesos zombis
- Los **zombis** se eliminan cuando el padre recoge el estado del hijo mediante `wait()`.
- En sistemas modernos, **init** o **systemd** maneja los huérfanos.

### Preguntas de comprensión:
1. **¿Qué es un proceso zombi?**
   - Un **proceso zombi** es un proceso que ha terminado, pero no se ha eliminado porque el proceso padre no ha recogido su estado mediante `wait()`.
   
2. **¿Cómo se puede evitar que los procesos huérfanos se conviertan en zombis?**
   - Usando `wait()` en el proceso padre o dejando que **init** se encargue de ellos.

