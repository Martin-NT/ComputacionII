# a) Fundamentos de procesos y programación concurrente
## 📘 1. ¿Qué es la programación concurrente?
Programación concurrente es un paradigma que permite ejecutar varias tareas al mismo tiempo. En sistemas operativos modernos, esto se traduce en la ejecución de múltiples procesos o hilos en paralelo, dependiendo de la arquitectura del software y hardware.

### 💡 ¿Por qué usar concurrencia?
- Mejor uso del CPU: Aprovecha múltiples núcleos del procesador.
- Mayor eficiencia: Tareas que no dependen entre sí pueden ejecutarse simultáneamente.
- Mejor rendimiento en I/O: Tareas como leer archivos, esperar respuestas de red, etc., no bloquean la ejecución del resto del programa.

## 🧠 2. Diferencia entre proceso e hilo
| Característica             | **Proceso**                            | **Hilo**                            |
| -------------------------- | -------------------------------------- | ----------------------------------- |
| Memoria                    | Aíslan su memoria entre sí             | Comparten la misma memoria          |
| Fallos                     | Un proceso que falla no afecta a otros | Un hilo puede afectar a otros hilos |
| Costo de creación          | Más pesado (más lento)                 | Más liviano (más rápido)            |
| Paralelismo real en Python | ✅ Sí                                   | ❌ No (por el GIL)                   |

### ✅ Ventajas y desventajas del multiprocessing en Python

### Ventajas:
- Permite paralelismo real (utiliza múltiples núcleos).
- Evita bloqueos por el GIL.
- Aislado: cada proceso tiene su memoria.

### Desventajas:
- Mayor consumo de memoria.
- Comunicación más compleja entre procesos que entre hilos.
- Overhead en la creación y destrucción de procesos.

### 🔄 Ciclo de vida de un proceso
1. **Creación**: Se instancia un nuevo proceso.
2. **Ejecución**: El proceso realiza su tarea.
3. **Esperando**: Puede esperar por recursos o comunicación.
4. **Finalización**: Termina su ejecución de forma natural o forzada.

### 💻 Ejemplo básico de creación de un proceso en Python
📁 Carpeta: Ejercicios
    - Archivo: primer_proceso.py

#### 🔍 Explicación:
- Se define una función worker().
- Se crea un proceso p con esa función como objetivo.
- .start() inicia el proceso.
- .join() espera a que el proceso termine.

### Preguntas de comprensión
1. ¿Cuál es la principal diferencia entre un proceso y un hilo en cuanto al uso de memoria?
Los procesos aíslan su memoria entre sí, mientras que los hilos comparten la misma memoria.

2. ¿Por qué multiprocessing puede aprovechar múltiples núcleos y threading no?
En Python (implementación CPython), existe un mecanismo llamado GIL (Global Interpreter Lock) que impide que más de un hilo ejecute código Python al mismo tiempo. Esto limita a los hilos a un solo núcleo de CPU.
En cambio, multiprocessing crea procesos independientes con su propio intérprete de Python, permitiéndoles ejecutarse en núcleos distintos del procesador.

3. ¿Qué función se usa para esperar a que un proceso termine?
`join()`  

# b) Creación y gestión de procesos con la biblioteca multiprocessing
## 📘 1. Crear un proceso con Process()
La forma más básica de usar multiprocessing es crear un objeto Process y pasarle como argumento una función a ejecutar. Ya vimos esto en el ejemplo anterior, pero ahora lo detallaremos mejor.

### 🔧 Métodos importantes de la clase Process
| Método        | Descripción                                            |
| ------------- | ------------------------------------------------------ |
| `start()`     | Inicia el proceso hijo                                 |
| `join()`      | El proceso padre espera a que el hijo termine          |
| `is_alive()`  | Devuelve `True` si el proceso sigue activo             |
| `terminate()` | Finaliza el proceso abruptamente (⚠ cuidado al usarlo) |
| `pid`         | Devuelve el PID (ID del proceso) del proceso hijo      |

### 🧩 Gestión de procesos padre e hijo
Cada proceso que creas con multiprocessing es un hijo del proceso que lo ejecuta (normalmente tu script Python). Python se encarga de hacer el fork (clon) del proceso, y el hijo tiene su propio espacio de ejecución.

### 🔍 Ejemplo práctico: crear y gestionar procesos
📁 Carpeta: Ejercicios
    - Archivo: gestion_procesos.py

#### 🔍 Qué debes observar en este ejemplo:
- Se crean dos procesos con diferentes argumentos.
- Se verifica si están activos con is_alive().
- Se usan join() para que el padre espere a ambos hijos.
- Cada proceso tiene un PID distinto.

### Preguntas de comprensión:
1. ¿Qué método permite saber si un proceso sigue corriendo?
`is_alive()` 

2. ¿Cuál es la función de join() en el proceso padre?
Esperar a que lso hijos terminen

3. ¿Qué diferencia hay entre start() y join()?
Que `start()` inicia al proceso hijo y `join()` hace que el proceso padre espere a que el hijo termine

# c) Comunicación entre procesos
## 📘 1. ¿Por qué es necesaria la comunicación?
Cuando trabajamos con múltiples procesos, cada proceso tiene su propia memoria. Esto significa que no pueden compartir directamente variables como sí lo harían los hilos. Para que los procesos compartan información, necesitamos usar mecanismos especiales.

## 🔗 2. Mecanismos principales en multiprocessing
### Pipes
- Conectan dos procesos para que se comuniquen.
- Permiten enviar y recibir datos como si fuera una tubería entre ellos.
- Se usan para comunicación entre dos procesos directamente.

### Queues
- Similar a una cola FIFO (first-in, first-out).
- Permiten que varios procesos coloquen y tomen datos de una cola compartida.
- Es el método más usado para comunicación entre múltiples procesos.

### 🔄 Diferencias entre Pipes y Queues
| Característica   | Pipes                                 | Queues                 |
| ---------------- | ------------------------------------- | ---------------------- |
| Nº de procesos   | 2 (conectados directamente)           | Múltiples              |
| Facilidad de uso | Requiere manejar extremos de conexión | Más simple             |
| Seguridad        | Menos seguro                          | Usa locks internamente |

### 💻 Ejemplo con Pipe
📁 Carpeta: Ejercicios
    - Archivo: pipe_basico.py

### 💻 Ejemplo con Queue
📁 Carpeta: Ejercicios
    - Archivo: queue_basico.py

### Preguntas de comprensión:
1. ¿Por qué los procesos no pueden compartir variables directamente?
nose
🔸 Porque cada proceso tiene su propia copia de la memoria.
A diferencia de los hilos, que comparten el mismo espacio de memoria, los procesos están aislados entre sí por el sistema operativo. Por eso necesitamos mecanismos como Pipe, Queue o memoria compartida para enviar datos entre ellos.

2. ¿Qué estructura es más adecuada para comunicar múltiples procesos: Pipe o Queue?
Queue: Es más flexible y segura para usar con más de dos procesos.

3. ¿Qué función se usa para recibir un mensaje desde un Pipe?
`recv()` 

# d) Sincronización básica con Lock
## 🧠 1. ¿Qué es un problema de concurrencia?
Cuando múltiples procesos acceden a un recurso compartido (como una variable o archivo) al mismo tiempo, pueden ocurrir errores inesperados. A esto lo llamamos condición de carrera (race condition).

### 🔍 Ejemplo de problema:
Dos procesos intentan sumar al mismo contador, pero terminan sobrescribiéndose mutuamente. El resultado final puede ser incorrecto.

## 🔐 2. ¿Qué es un Lock?
Un Lock es un candado que usamos para proteger secciones críticas del código. Solo un proceso a la vez puede entrar en esa sección cuando el lock está activado.

- lock.acquire() → toma el candado
- lock.release() → libera el candado

Python también permite usarlo con with para mayor seguridad.

### 💻 Ejemplo sin Lock (hay error)
📁 Carpeta: Ejercicios
    - Archivo: contador_sin_lock.py

🔴 El resultado esperado es 200000, pero muchas veces será menor debido a condiciones de carrera.
/contador_sin_lock.py
Contador final: 112063

### 💻 Ejemplo con Lock (resultado correcto)
📁 Carpeta: Ejercicios
    - Archivo: contador_con_lock.py

✅ Ahora sí el valor final es consistentemente 200000.
/contador_con_lock.py
Contador final: 200000

### Preguntas de comprensión:
1. ¿Qué es una condición de carrera?
Es una situación que ocurre cuando dos o más procesos acceden al mismo recurso compartido (como una variable) al mismo tiempo, y el resultado depende del orden en que se ejecuten.
🔴 Esto puede provocar resultados incorrectos o inesperados
Ejemplo real:
Dos procesos suman 1 a un contador al mismo tiempo → uno pisa el valor del otro → el contador no suma bien.

2. ¿Para qué sirve un Lock?
Para proteger secciones críticas del código.
Solo un proceso a la vez puede ejecutar ese bloque cuando usamos Lock. Así evitamos condiciones de carrera.

3. ¿Qué diferencia ves en el resultado al usar o no usar Lock?
Sin Lock, el contador puede terminar con un valor incorrecto (como 162381 en lugar de 200000).
Con Lock, el resultado es siempre el esperado, porque los procesos no se pisan entre sí.

# e) Pool de procesos

## 🤔 ¿Qué es un Pool?
Un Pool (grupo) nos permite crear un conjunto fijo de procesos y reutilizarlos para ejecutar varias tareas en paralelo.
Esto es útil cuando tenés muchas tareas pequeñas y no querés crear un proceso nuevo para cada una (lo cual consume más recursos).

### ✅ Ventajas de usar Pool
- Reutiliza procesos, ahorrando tiempo y memoria.
- Simplifica la distribución de tareas.
- Permite ejecutar funciones en paralelo de forma muy clara.

### 🧰 Métodos más comunes
| Método                 | Descripción                                                                   |
| ---------------------- | ----------------------------------------------------------------------------- |
| `map(func, iterable)`  | Aplica `func` a cada elemento del iterable. Devuelve los resultados en orden. |
| `apply(func, args=())` | Ejecuta `func(*args)` en **un** proceso del pool.                             |
| `map_async()`          | Igual que `map` pero **asíncrono** (devuelve un objeto especial, no bloquea). |
| `apply_async()`        | Igual que `apply` pero **asíncrono**.                                         |

## 💪 Ejemplos prácticos
### 💻 Ejemplo básico con map()
📁 Carpeta: Ejercicios
    - Archivo: pool_map.py

#### 🧠 ¿Qué hace?
- Crea un Pool de 2 procesos.
- Ejecuta la función cuadrado() en paralelo con cada número de la lista.
- Devuelve los cuadrados de los números.

### 💻 Ejemplo con apply_async()
📁 Carpeta: Ejercicios
    - Archivo: pool_apply_async.py

#### 🧠 ¿Qué hace?
- Ejecuta la función saludar() para cada nombre en paralelo.
- Usa apply_async() para no esperar el resultado (como en una notificación).

### 💪 Ejercicio práctico
📁 Carpeta: Ejercicios
    - Archivo: pool_ejercicio.py

📝 Objetivo: Crear una función que reciba un número y devuelva su factorial. Usá Pool.map() para calcular los factoriales de [5, 6, 7, 8].

## Preguntas de comprensión:
1. ¿Qué ventaja tiene usar Pool frente a crear procesos manualmente?
Crear procesos uno por uno con Process() puede ser más lento y consumir más memoria, especialmente si hay muchas tareas.
👉 Pool permite reutilizar un número fijo de procesos, lo que mejora el rendimiento y hace que el código sea más simple y ordenado.

2. ¿Qué diferencia hay entre map() y apply_async()?
| Característica      | `map()`                            | `apply_async()`                           |
| ------------------- | ---------------------------------- | ----------------------------------------- |
| Tipo de ejecución   | Bloqueante (espera resultados)     | No bloqueante (sigue sin esperar)         |
| Ideal para          | Aplicar una función a varios datos | Tareas individuales sin esperar respuesta |
| Devuelve resultados | Sí (lista de resultados ordenada)  | Sí (pero mediante un objeto especial)     |
| Uso común           | Procesamiento de datos en lote     | Notificaciones o tareas en segundo plano  |

3. ¿Qué hace pool.join()?
Espera a que todas las tareas del Pool terminen.
👉 Siempre se usa después de pool.close() para asegurarse de que todo el trabajo haya finalizado antes de seguir.

# f) Memoria compartida básica
Cuando trabajamos con multiprocessing, cada proceso tiene su propio espacio de memoria.
Esto significa que no pueden compartir variables directamente (a diferencia de los hilos).
Pero Python ofrece una solución: las estructuras Value y Array, que permiten compartir memoria de forma segura entre procesos.

## 🧠 ¿Qué son Value y Array?
- Value: permite compartir una sola variable (por ejemplo, un entero).
- Array: permite compartir una lista de valores (por ejemplo, una lista de enteros).
Ambas vienen del módulo multiprocessing y permiten el acceso seguro entre procesos.

### 💡 Sintaxis
```bash
from multiprocessing import Value, Array

# Crear una variable entera compartida con valor inicial 0
contador = Value('i', 0)

# Crear un array de 5 elementos enteros
numeros = Array('i', [1, 2, 3, 4, 5])

```
📌 El primer parámetro indica el tipo:
- 'i': entero
- 'd': float
- 'c': caracter

### 💻 Ejemplo 1: Uso básico de Value
📁 Carpeta: Ejercicios
    - Archivo: memoria_value.py

⚠️ Problema: Este ejemplo no usa Lock, así que puede haber condición de carrera. Lo corregiremos más adelante.

### 💻 Ejemplo 2: Uso básico de Array
📁 Carpeta: Ejercicios
    - Archivo: memoria_array.py

✅ En este caso, como solo un proceso accede al array, no hay conflicto.

## Preguntas de comprensión
1. ¿Por qué no podemos compartir variables normales entre procesos?
Porque cada proceso en Python tiene su propia memoria aislada.
Cuando se crea un proceso nuevo, se copia el estado del proceso padre, pero luego cada uno trabaja con su propia copia.

🔐 Esto significa que:
- Si un proceso cambia una variable, los demás no lo ven.
- No existe una memoria compartida como en los hilos.
📌 Por eso usamos estructuras especiales como Value y Array.

2. ¿Qué diferencia hay entre Value y Array?
| Característica | `Value`                          | `Array`                     |
| -------------- | -------------------------------- | --------------------------- |
| Tipo de dato   | Un solo valor (por ejemplo, int) | Varios valores (una lista)  |
| Uso típico     | Contadores, flags                | Listas de datos compartidos |
| Ejemplo        | `Value('i', 0)`                  | `Array('i', [1, 2, 3])`     |

3. ¿Para qué sirve el primer parámetro ('i', 'd', etc.) al crear un Value o Array?
Este parámetro indica el tipo de dato que se va a guardar en memoria compartida. Es como decirle a Python qué tipo de número o dato va a manejar:
| Código | Significa              |
| ------ | ---------------------- |
| `'i'`  | entero (int)           |
| `'d'`  | número decimal (float) |
| `'c'`  | caracter (bytes/char)  |
✅ Esto es necesario porque multiprocessing trabaja con tipos de bajo nivel, más cercanos al sistema operativo.

# 🧪 Actividad final: mp_worker.py

## 🎯 Objetivo
Modificar un script para que varios procesos trabajen en paralelo, y así mostrar que se ejecutan al mismo tiempo, no uno después del otro.

📁 Carpeta: Ejercicios
    - Archivo: mp_worker_sin_modificar.py
    - Archivo: mp_worker_modificado.py

## 📌 Instrucciones
1. Correr primero este script mp_worker_sin_modificar.py (funciona de forma secuencial).
2. Verás que toma alrededor de 4 segundos en total.
3. Luego, modifícalo para usar multiprocessing, creando dos procesos en mp_worker_modificado.py

✅ Este cambio hace que ambas tareas se ejecuten en paralelo, reduciendo el tiempo total a unos 2 segundos, demostrando paralelismo real.

### 🧠 ¿Cómo sabrás que funciona?
- Si el tiempo total es cercano a 2 segundos, ¡lo lograste!
- Si sigue siendo cercano a 4, algo no está corriendo en paralelo (verificá start() y join()).

### ⏱️ Resultados
- Tiempo total esperado: ~2 segundos
- Tiempo real obtenido: (completá con el resultado de tu ejecución)
✅ La reducción del tiempo demuestra que los procesos se ejecutan en paralelo

### 🧠 Reflexión personal 
Este ejercicio me permitió entender cómo multiprocessing puede acelerar tareas al ejecutarlas en paralelo. Fue clave usar Process, start() y join(), y ver la diferencia concreta al medir el tiempo de ejecución.