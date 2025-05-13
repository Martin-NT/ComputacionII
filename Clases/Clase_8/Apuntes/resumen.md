# 🧠 Resumen de Multiprocessing en Python

## 📌 Fundamentos de Procesos y Programación Concurrente

- **Proceso**: unidad de ejecución con memoria propia. Aislamiento total.
- **Hilo (thread)**: unidad de ejecución dentro de un proceso. Comparte memoria con otros hilos.
- **Multiprocessing vs Threading**:
  - *Multiprocessing* aprovecha múltiples núcleos físicos → paralelismo real.
  - *Threading* en Python no logra paralelismo real por el GIL (Global Interpreter Lock).
- **Ciclo de vida de un proceso**:
  1. Creación
  2. Inicio con `start()`
  3. Ejecución
  4. Terminación (esperada con `join()`)

## 🧱 Creación y Gestión de Procesos

- Clase `Process` del módulo `multiprocessing` permite crear procesos.
- Métodos clave:
  - `start()`: inicia el proceso
  - `join()`: espera a que el proceso termine
  - `is_alive()`: devuelve `True` si el proceso sigue corriendo
- Cada proceso tiene su propio PID (Process ID).
- Ejemplo: ver carpeta `Ejercicios/procesos/procesos.py`

## 🔄 Comunicación entre Procesos

- Los procesos no comparten memoria directamente.
- **Pipes** (`Pipe()`):
  - Conexión punto a punto.
  - Métodos: `send()`, `recv()`
- **Queues** (`Queue()`):
  - Cola segura entre múltiples procesos.
  - Métodos: `put()`, `get()`
- ¿Cuál usar?
  - `Queue` es más flexible y adecuada para múltiples productores/consumidores.
- Ejemplo: ver carpeta `Ejercicios/pipe_queue/pipe_queue.py`

## 🔐 Sincronización con Lock

- **Condición de carrera**: cuando múltiples procesos acceden a una misma sección crítica al mismo tiempo y producen resultados incorrectos.
- Solución: **Lock** (`Lock()`)
  - `lock.acquire()` para entrar
  - `lock.release()` para salir
  - O usar `with lock:` para mayor seguridad
- Evita conflictos al modificar recursos compartidos.
- Ejemplo: ver carpeta `Ejercicios/lock/lock.py`

## 🌀 Pool de Procesos

- `Pool`: administra un conjunto fijo de procesos para tareas paralelas.
- Métodos:
  - `map(func, iterable)`: aplica `func` a cada elemento
  - `apply(func, args)`: llama a `func` con `args`
  - `map_async()` / `apply_async()`: versiones no bloqueantes
- Ventaja: reutilización de procesos, más eficiente.
- Ejemplo: ver carpeta `Ejercicios/pool/pool.py`

## 🧮 Memoria Compartida con Value y Array

- Usar `Value` y `Array` permite compartir datos simples entre procesos.
- Necesitan especificar tipo de dato:
  - `'i'`: int
  - `'d'`: float
  - `'c'`: char
- Ejemplo:
  ```python
  from multiprocessing import Value
  v = Value('i', 0)
  v.value += 1
