# Señales en Sistemas Operativos: Un Mecanismo Asíncrono de Comunicación entre Procesos
## ✅ Tema 1: ¿Qué son las señales y por qué son importantes?
### 1. 📚 Explicación Teórica
Las señales son un mecanismo fundamental del sistema operativo (especialmente en sistemas UNIX y POSIX) para comunicar eventos asincrónicos a procesos. Actúan como interrupciones software: notifican a un proceso que ha ocurrido una situación que requiere su atención inmediata.

#### 🔧 Definición formal:
Una señal es una notificación que el kernel del sistema operativo envía a un proceso para indicarle que ha ocurrido un evento, como una división por cero, intento de acceder a memoria inválida, o la recepción de una interrupción externa (ej. Ctrl+C).

#### ¿Por qué son importantes?
    - Permiten manejar errores y excepciones a bajo nivel.
    - Son esenciales en la comunicación entre procesos (IPC).
    - Se utilizan para terminar, pausar o reanudar procesos.
    - Son fundamentales en sistemas concurrentes y en programación de bajo nivel, donde los hilos o procesos necesitan reaccionar rápidamente a eventos.

### 2. 🧪 Tipos de señales
|      Tipo       |                            Características                                                          |
|-----------------------------------------------------------------------------------------------------------------------|
|  **Síncronas**  | Generadas por el proceso al ejecutar una instrucción ilegal. Ej: `SIGFPE`, `SIGSEGV`.               |
| **Asíncronas**  | Generadas externamente (otro proceso o el kernel). Ej: `SIGINT`, `SIGTERM`.                         |
| **Tiempo real** | Parte del estándar POSIX.1b. Se pueden **encolar**, tienen **prioridad definida**.                  |

### 3. ⚙️ ¿Qué ocurre internamente?
Cuando una señal llega a un proceso, el sistema operativo:
    1. Interrumpe su flujo normal de ejecución.
    2. Verifica si tiene un manejador de señal (signal handler) registrado.
    3. Si lo tiene, ejecuta ese manejador.
    4. Si no, aplica la acción predeterminada (por ejemplo, terminar el proceso).

### 4. 🛠 Instrucciones prácticas paso a paso (Sin código aún)
A nivel práctico, como desarrollador:
    1. Identificás qué señales te interesan (por ejemplo, SIGINT para capturar Ctrl+C).
    2. Registrás una función propia que se ejecutará cuando llegue esa señal.
    3. Probás el sistema enviando señales manualmente (con kill) o con eventos reales.

#### 💻 Ejemplo de código (conceptual por ahora)
```bash
import signal

def handler(signum, frame):
    print(f"¡Señal recibida! Código: {signum}")

signal.signal(signal.SIGINT, handler)

while True:
    pass  # El proceso se queda corriendo esperando Ctrl+C
```
➡️ Este código define un manejador personalizado para SIGINT. Cuando se presiona Ctrl+C, en vez de cerrar el programa, se ejecuta el handler.

### 5. 🧠 Ejercicios prácticos
1. Explicá con tus palabras qué es una señal y cuándo se usa SIGINT.
Una señal es un mensaje que el sistema operativo le envía a un proceso para avisarle que ocurrió algo importante. Por ejemplo, cuando presionás Ctrl+C en la terminal, se envía la señal SIGINT (Signal Interrupt) al proceso que está corriendo. Esta señal le indica al proceso que debería interrumpirse o terminarse.

🧠 En resumen:
    Una señal es como una notificación urgente del sistema operativo hacia un programa. SIGINT se usa cuando el usuario quiere interrumpir un programa manualmente.

2. Diferencia entre SIGTERM y SIGKILL. Cuadro comparativo:

| Característica      | `SIGTERM`                   | `SIGKILL`                     |
| ------------------- | --------------------------- | ----------------------------- |
| Código de señal     | `15`                        | `9`                           |
| ¿Se puede capturar? | ✅ Sí, se puede manejar      | ❌ No, no se puede bloquear    |
| Acción por defecto  | Terminar el proceso         | Matar el proceso de inmediato |
| Uso típico          | Cierre ordenado del proceso | Finalización forzada          |

📌 Resumen:
    - **SIGTERM** es una forma educada de pedirle a un proceso que termine.
    - **SIGKILL** es una orden brusca: el sistema operativo mata el proceso sin que pueda defenderse.

3. Si desarrollás un servidor, ¿qué señales deberías capturar y por qué?
Si estoy desarrollando un servidor, me interesa capturar señales como:
    - **SIGINT (Ctrl+C)** → Para cerrar el servidor de forma segura y liberar recursos.
    - **SIGTERM** → Para manejar cierres programados (como reinicios del sistema).
    - **SIGHUP** → Para recargar configuración sin apagar el servidor.
    - **SIGCHLD** → Si tengo procesos hijos (por ejemplo, subprocesos para manejar conexiones), esta señal me avisa cuando terminan.

🧠 En resumen:
    Capturar estas señales me permite tener un servidor robusto, que no se caiga mal ni pierda datos al cerrarse.

### 6. Preguntas
1. ¿Qué diferencia hay entre una señal síncrona y una asíncrona?

| Tipo de señal | ¿Quién la genera?                   | Ejemplo                      |
| ------------- | ----------------------------------- | ---------------------------- |
| **Síncrona**  | El propio proceso, por error        | División por cero (`SIGFPE`) |
| **Asíncrona** | Otro proceso o el sistema operativo | `Ctrl+C` (`SIGINT`)          |

🔎 Más claro:
    - **Síncrona**: Ocurre durante la ejecución de una instrucción en tu código. Es directamente causada por el proceso.
    - **Asíncrona**: Viene de fuera del proceso. Por ejemplo, el usuario u otro programa.

2. ¿Por qué el sistema operativo necesita interrumpir un proceso con señales?

📌 Porque las señales permiten:
    - Avisar que ocurrió un evento crítico (como error o cierre).
    - Sincronizar procesos, como en multitarea.
    - Liberar recursos cuando un proceso hijo termina.
    - Permitir que el usuario o el sistema tenga control sobre los procesos activos.

🧠 Pensalo como un botón de emergencia: cuando pasa algo importante, el sistema tiene que asegurarse de que el proceso se entere.

3. ¿Qué puede pasar si no se manejan adecuadamente las señales?

📌 Si no las manejás bien, puede ocurrir:
    - Que el proceso se cierre inesperadamente.
    - Que pierdas datos por no guardar estados antes de terminar.
    - Que queden recursos colgados (memoria, archivos abiertos, puertos).
    - Que no puedas hacer sincronización entre procesos correctamente.

🛑 En entornos concurrentes, no manejar señales puede llevar a condiciones de carrera o deadlocks.

## ✅ Tema 2: signal.signal() y funciones relacionadas en Python

### 1. 📚 Explicación Teórica
Python, al estar basado en sistemas POSIX (como Linux y macOS), permite manipular señales del sistema operativo a través del módulo signal.

#### 🧠 ¿Qué es signal.signal()?
Es la función principal para asociar una señal del sistema con una función (llamada handler o manejador).
Cuando el proceso recibe esa señal, se interrumpe su ejecución normal y ejecuta la función que vos definiste.

#### 🔧 ¿Cómo funciona internamente?
Cuando llamás a:
```bash
signal.signal(signal.SIGINT, handler)
```

Estás diciéndole al sistema:
    "Cuando llegue una SIGINT (ej. presionar Ctrl+C), en vez de terminar el programa, ejecutá esta función que yo definí como handler."

Este handler debe tener esta firma:
```bash
def handler(signum, frame):
    ...
```

Donde:
    - **signum**: número de señal recibido (por ejemplo, 2 para SIGINT).
    - **frame**: el contexto de ejecución actual (no lo usás mucho, pero es obligatorio incluirlo).

### 2. 🛠 Instrucciones prácticas paso a paso
    1. Importá el módulo signal.
    2. Definí un handler (función que se llama cuando llega la señal).
    3. Asociá la señal con tu handler usando signal.signal().
    4. Mantené el programa corriendo (con un bucle o un sleep).
    5. Probá enviando señales (ej. Ctrl+C o kill).

#### 💻 Ejemplo básico comentado
📁 Carpeta: practica_signals_apunte
    - Archivo: 00_ejemplo_basico_signal.py

🧪 Probalo desde la terminal, y verás que al presionar Ctrl+C, no se termina el programa, sino que muestra el mensaje de advertencia.

### 3. 🔁 Funciones relacionadas
| Función                    | Descripción breve                                       |
| -------------------------- | ------------------------------------------------------- |
| `signal.signal(sig, func)` | Asocia una señal con una función personalizada          |
| `signal.getsignal(sig)`    | Devuelve la función asociada actualmente a una señal    |
| `signal.raise_signal(sig)` | Envia la señal desde el **propio proceso**              |
| `signal.SIG_IGN`           | Valor especial para **ignorar** una señal               |
| `signal.SIG_DFL`           | Valor especial para restaurar la acción **por defecto** |

### 4. 🧪 Ejercicios prácticos
1. Modificá el handler para que imprima un mensaje distinto por cada tipo de señal (SIGINT,SIGTERM, etc.).
- Captura y maneja señales como SIGINT y SIGTERM.
- Usa `signal.signal()` para personalizar el comportamiento.
- Probalo con Ctrl+C o enviando señales con `kill`.

📁 Carpeta: practica_signals_apunte
    - Archivo: 01_signal_basico.py


2. Escribí un programa que ignore SIGINT por 10 segundos y luego vuelva al comportamiento normal.
- Ignora Ctrl+C durante 10 segundos.
- Luego restablece el handler personalizado.

📁 Carpeta: practica_signals_apunte
    - Archivo: 02_ignorar_SIGINT.py


3. Combiná el uso de signal con multiprocessing.Process para que un proceso padre capture SIGINT y avise al hijo para que termine correctamente.
- Usa `multiprocessing` para crear un hijo.
- El padre maneja SIGINT y termina al hijo correctamente.

📁 Carpeta: practica_signals_apunte
    - Archivo: 03_signal_multiproceso.py

### 5. Preguntas
1. ¿Qué hace signal.signal() y cuál es su propósito?

📌 Permite asociar una señal específica (como SIGINT) con una función personalizada (handler) que se ejecuta cuando esa señal llega.
Sirve para que el programa tome control del comportamiento ante eventos críticos como interrupciones o terminación.

2. ¿Qué pasaría si no definís ningún handler y presionás Ctrl+C?

📌 Si no definís un handler para SIGINT, el sistema operativo ejecuta la acción por defecto, que en el caso de SIGINT es terminar el proceso inmediatamente.
Con un handler, podés personalizar la respuesta, como guardar datos antes de cerrar o ignorar la señal si es necesario.

3. ¿Por qué es útil poder interceptar una señal en un programa?

📌 Porque:
    - Permite hacer un cierre ordenado (guardar archivos, liberar recursos, avisar a otros procesos).
    - Podés prevenir cierres accidentales por parte del usuario.
    - Es clave para procesos críticos, servidores o tareas de largo plazo, donde no se puede perder el estado por una interrupción inesperada.

## ✅ Tema 3: kill, sigqueue y sigaction (con referencias cruzadas a C)

### 1. 📚 Explicación conceptual
En sistemas UNIX y POSIX, las señales no se envían solo por el teclado (como Ctrl+C). También se pueden:
    - Enviar desde otros procesos usando funciones del sistema.
    - Controlar más finamente (con información adicional, prioridad, etc.).

A continuación, tres mecanismos fundamentales:
| Función                     | Lenguaje  | ¿Qué hace?                                                                      |
| --------------------------- | --------- | ------------------------------------------------------------------------------- |
| `kill(pid, sig)`            | C / Shell | Envía una señal a un proceso específico. No es solo para “matar” procesos.      |
| `sigqueue(pid, sig, valor)` | C         | Envía una señal con un valor adicional (solo para señales de tiempo real).      |
| `sigaction()`               | C         | Reemplaza `signal()` con una forma más potente y controlada de manejar señales. |

### 🛠️ 2. Instrucciones prácticas con Python
Aunque sigqueue y sigaction son parte de C, en Python podés trabajar con señales desde el punto de vista del receptor, y usar os.kill() para enviarlas.

Vamos a usar os.kill() como equivalente de kill.

#### Comparación de funciones: kill vs sigqueue
Aunque en Python puro no se usa sigqueue, es importante entender su diferencia con kill, especialmente si más adelante vas a programar en C.

| Función    | ¿Permite enviar datos?           | ¿Requiere señal de tiempo real? | ¿Disponible en Python? |
| ---------- | -------------------------------- | ------------------------------- | ---------------------- |
| `kill`     | ❌ No                             | ❌ No                            | ✅ (via `os.kill()`)    |
| `sigqueue` | ✅ Sí (estructura `union sigval`) | ✅ Sí                            | ❌ No directamente      |

#### Ejemplo de código con os.kill() en Python
📁 Carpeta: practica_signals_apunte
    - Archivo: 04_os_kill_envio.py

🟢 Enviando señales entre procesos
- Ejecuta el codigo
- Abrí una terminal adicional y ejecutá:
```bash
kill -SIGUSR1 <PID_DEL_SCRIPT>
```
🔁 Esto simula cómo otro proceso puede enviar señales.


### 4. Preguntas
1. ¿Qué función podés usar en Python para enviar una señal a otro proceso?
```bash
os.kill(pid, señal)
```
En Python, usamos os.kill() para enviar una señal a un proceso identificado por su PID (Process ID). A pesar del nombre, no solo sirve para “matar” procesos, sino también para enviar señales como SIGUSR1, SIGINT, etc.

Ejemplo real:
```bash
import os, signal
os.kill(12345, signal.SIGUSR1)
```
2. ¿Qué diferencia hay entre kill y sigqueue?

| Característica                   | `kill()`                             | `sigqueue()`                                      |
| -------------------------------- | ------------------------------------ | ------------------------------------------------- |
| **Envia datos con la señal**     | ❌ No                                | ✅ Sí (puede adjuntar un valor entero o puntero)  |
| **Requiere señales tiempo real** | ❌ No, funciona con señales estándar | ✅ Sí, usa señales tipo `SIGRTMIN + n`            |
| **Complejidad**                  | Simpler, tradicional                 | Más potente, pero más compleja de usar            |
| **Disponible en Python**         | ✅ Sí (`os.kill()`)                  | ❌ No directamente disponible                     |

Resumen:
kill() es simple y directo, pero no permite enviar información adicional. sigqueue() es más moderno (POSIX.1b), permite adjuntar datos, pero solo funciona con señales de tiempo real y solo en C.

3. ¿Por qué sigaction es más seguro que signal() en C?
Porque sigaction() te da más control y evita comportamientos inesperados que pueden ocurrir con signal().

Explicación detallada:

**signal()** es una función antigua. En algunas implementaciones de UNIX, el handler se restaura automáticamente al valor por defecto después de una señal, lo que puede generar errores difíciles de detectar.

**sigaction()** te permite:
    - Establecer flags de comportamiento más fino (SA_RESTART, SA_SIGINFO).
    - Recibir información adicional sobre la señal con siginfo_t.
    - Controlar qué otras señales se bloquean mientras se ejecuta el handler.
    - Ser async-signal-safe, es decir, seguro para señales en contextos críticos.

Por eso, sigaction() es la forma recomendada en sistemas modernos, aunque es más verbosa que signal().

## ✅ Tema 4: Uso de señales para sincronizar procesos

### 1. 📚 Explicación conceptual
En sistemas operativos, los procesos pueden sincronizarse entre sí usando distintos mecanismos (pipes, sockets, memoria compartida, etc.). Las señales son uno de los más simples y ligeros.

#### ¿Qué significa "sincronizar procesos"?
Que un proceso espere, reaccione o coordine su comportamiento en función de otro. Por ejemplo:
    - Un proceso padre espera una señal del hijo para continuar.
    - Un proceso hijo se detiene hasta recibir SIGUSR1 desde otro proceso.
    - Un proceso usa SIGALRM para saber cuándo detenerse (temporización).

#### 🧠 Ventajas de las señales para sincronizar:
- Muy livianas (no requieren mucha memoria).
- Asíncronas: el proceso puede estar haciendo otra cosa mientras espera.
- Disponibles en todos los sistemas UNIX.

#### ⚠️ Limitaciones:
- Las señales no transportan datos (salvo sigqueue en C).
- No garantizan orden si varias llegan a la vez.
- No sirven para comunicación compleja o estructurada (ahí se usan pipes, sockets, etc.).

### 2. 🛠️ Instrucciones prácticas
Vamos a hacer que:
    - Un proceso hijo espere una señal del padre.
    - El padre le mande SIGUSR1 cuando debe continuar.

#### ✅ Ejemplo comentado: sincronización simple con señales
📁 Carpeta: practica_signals_apunte
    - Archivo: 05_sincronizacion_basica.py

#### 📌 ¿Qué hace este código?
- El hijo se detiene hasta que reciba la señal.
- El padre espera 3 segundos y luego la envía.
- Esto es un ejemplo real de sincronización por señal entre procesos usando fork().
💡 signal.pause() es una función que bloquea la ejecución hasta recibir una señal válida.

#### 3. 🧪 Ejercicios propuestos
1. Modificá el código para que el padre envíe SIGINT en lugar de SIGUSR1. ¿Qué cambia?
📁 Carpeta: practica_signals_apunte
    - Archivo: 06_sincronizacion_sigint.py

✅ ¿Qué cambia?
Nada esencial en la lógica, solo que ahora se intercepta SIGINT. Esto demuestra que podemos elegir qué señal usar, siempre que el receptor la maneje.

2. Hacé que el hijo reaccione de forma diferente según reciba SIGUSR1 o SIGUSR2.
📁 Carpeta: practica_signals_apunte
    - Archivo: 07_dos_signals.py

✅ Resultado esperado:
```bash
🟢 Hijo recibió SIGUSR1: Acción A
🔵 Hijo recibió SIGUSR2: Acción B
```

3. Implementá una secuencia donde:
- El hijo hace tres pausas.
- El padre le manda tres señales (SIGUSR1) con tiempo entre ellas.
- El hijo imprime un número diferente cada vez (como si fuera una “cuenta regresiva”).

📁 Carpeta: practica_signals_apunte
    - Archivo: 08_cuenta_regresiva.py

✅ Esto muestra:
```bash
🔔 Señal recibida. Cuenta: 3
🔔 Señal recibida. Cuenta: 2
🔔 Señal recibida. Cuenta: 1
✅ ¡Cuenta regresiva terminada!
```
#### 4. Preguntas
1. ¿Qué hace signal.pause()?
Suspende la ejecución del proceso hasta que reciba una señal válida.

Explicación:
Es una manera segura y eficiente de "esperar una señal". No consume CPU como un bucle de espera activa.

2. ¿Qué pasaría si el padre manda la señal antes de que el hijo la espere?
La señal se pierde si no hay un handler registrado aún o si el proceso no está esperando con pause().

Explicación:
Las señales estándar no se encolan. Si un proceso no está preparado, la señal puede ser ignorada o tener comportamiento por defecto, como terminar el proceso.

💡 Solución típica: asegurar que el hijo instale el handler antes de que el padre actúe.

3. ¿Por qué este método no sirve si necesitás pasarle un número o texto al hijo?
Porque las señales estándar no transportan datos.

Explicación:
Las señales como SIGUSR1 solo indican un evento, no llevan información. Para eso se usan:
    - sigqueue() en C (con sigval)
    - O mecanismos como pipes o sockets si estás en Python.

## ✅ Tema 4: Manejo seguro de señales y async-signal-safety

### 1. 📚 Explicación conceptual
Cuando una señal interrumpe un proceso, se ejecuta su handler (función que definiste con signal.signal() o sigaction()). Pero no todo código es seguro de ejecutar dentro de ese handler, porque:
    - Las señales pueden llegar en cualquier momento, incluso mientras se ejecutan operaciones críticas (como escritura en archivos, uso de memoria compartida, o llamadas de sistema).

    - Si usás funciones que no son reentrantes (que no se pueden interrumpir y volver a ejecutar sin errores), podés corromper el estado del programa.

Por eso, existe un concepto clave:

#### 🔒 ¿Qué es async-signal-safe?
Es una propiedad que tienen algunas funciones del sistema que las hace seguras para llamar dentro de un handler de señal.
➡️ Por ejemplo:
    - ✅ write(), read(), _exit(), kill()
    - ❌ printf(), malloc(), strtok(), open() (¡pueden romper todo!)

#### 🔥 Ejemplo de riesgo:
```java
// C - Peligroso
void handler(int sig) {
    printf("Señal recibida\n"); // ❌ No async-signal-safe
}
```

Este código podría fallar si printf() usa internamente memoria que está siendo modificada cuando llega la señal.

#### 🧠 En Python esto también aplica
Python es más seguro porque:
    - Su intérprete maneja las señales de forma diferida (no interrumpe en cualquier punto).
    - Pero no se garantiza comportamiento seguro si hacés cosas complejas dentro del handler (como abrir archivos o usar threads).

💡 En handlers de señal de Python, lo mejor es solamente cambiar una variable de estado y dejar que el proceso principal la revse.

### 2. 🧪 Ejemplo correcto en Python
📁 Carpeta: practica_signals_apunte
    - Archivo: 09_async_safe.py

#### ✅ Claves de diseño seguro
- Dentro de un handler, no escribas archivos, no uses sockets ni stdout.
- Solo poné una bandera (True/False) o usá funciones como os._exit() si tenés que terminar rápido.
- Manejá la lógica completa fuera del handler, en el programa principal.

### 3. 🧪 Ejercicios prácticos

1. Reescribí un handler que solo ponga una variable global en True y hacé que el programa principal actúe en consecuencia.

📁 Carpeta: practica_signals_apunte
    - Archivo: 10_flag_handler.py

📝 Probalo desde otra terminal:
```bash
kill -SIGUSR1 <PID>
```

2. Creá un programa que escriba cada segundo en pantalla, y se detenga solo cuando reciba una señal. Asegurate de no usar print() en el handler.

📁 Carpeta: practica_signals_apunte
    - Archivo: 11_salida_controlada.py

🧠 Diferencia clave: el handler no imprime nada, solo marca un estado.

3. Diseñá un sistema donde el handler de señal activa una interrupción controlada (por ejemplo, simular apagar un motor). El handler no debe hacer nada más que marcar que se recibió la orden.

📁 Carpeta: practica_signals_apunte
    - Archivo: 12_simulacion_apagado.py

📢 Desde otro terminal, simulás la señal de emergencia:
```bash
kill -SIGUSR2 <PID>
```
### 4. Preguntas
1. ¿Por qué no es seguro usar print() dentro de un handler?
Porque print() no es una función async-signal-safe. Internamente puede usar buffers, malloc() o acceder a estructuras de datos compartidas, y si una señal interrumpe ese proceso, puede dejar el programa en un estado inconsistente o provocar errores como segmentation fault.

🧠 Lo seguro es usar funciones mínimas como write() o modificar flags.

2. ¿Cuál es la mejor práctica para reaccionar a señales en Python?
Usar el handler para cambiar una variable global simple (por ejemplo, un booleano como detener = True), y dejar que el proceso principal revise ese estado y decida cómo actuar.

🔁 Este patrón es seguro, predecible y compatible con el modelo de ejecución de Python (que no interrumpe en cualquier momento).

3. ¿Qué podría pasar si modificás estructuras de datos complejas dentro de un handler?
Podrías corromper el estado interno del programa.
Ejemplo: si un handler modifica un diccionario o lista mientras otro hilo lo está recorriendo, podés causar errores como:
    - Condiciones de carrera.
    - Caídas por RuntimeError.
    - Datos parcialmente escritos o perdidos.

📛 Regla de oro: en el handler, hacé lo mínimo indispensable.

## ✅ Tema 5: Señales en Sistemas Multihilo (Multithreaded)

### 1. 📚 Explicación conceptual
En un programa multihilo, hay varios hilos (threads) ejecutándose dentro de un mismo proceso. Cada hilo comparte el mismo espacio de memoria, pero puede tener distinto estado de ejecución.

💡 Las señales en sistemas multihilo (como en Linux) no se entregan automáticamente a todos los hilos, sino que:
| 🔍 Situación                      | ¿A qué hilo se entrega la señal?                        |
| --------------------------------- | ------------------------------------------------------- |
| Enviada al proceso (ej: `SIGINT`) | El sistema elige un hilo que **no la tenga bloqueada**. |
| Enviada directamente a un hilo    | Con funciones como `pthread_kill()` en C.               |
| Señales síncronas (ej: `SIGSEGV`) | Se entregan **al hilo que provocó la falla**.           |

### 2. ⚠️ Problemas frecuentes
- Si varios hilos manejan señales, pueden interferir o ignorar señales si no están correctamente configurados.
- En Python (usando el módulo threading), solo el hilo principal recibe señales.

### 3. ✅ Buenas prácticas en Python
- Instalar handlers de señales solo en el hilo principal.
- Usar flags compartidos, Event(), Queue() u otros mecanismos para comunicar a los demás hilos que se recibió una señal.

### 4. 🧪 Ejercicios prácticos
1. Ejemplo en Python con hilos
📁 Carpeta: practica_signals_apunte
    - Archivo: 13_multithread_signal_safe.py

👆 Ejecutalo y luego presioná Ctrl+C para enviar SIGINT.

#### 🧠 ¿Qué aprendiste con este ejemplo?
- Aunque hay varios hilos, solo el hilo principal maneja la señal.
- Usamos threading.Event() como un canal seguro y compartido para notificar a los otros hilos.

2. Modificá el ejemplo para que tenga 3 hilos en vez de 2, y todos terminen cuando el usuario presione Ctrl+C.
📁 Carpeta: practica_signals_apunte
    - Archivo: 14_tres_hilos_sigint.py

🧪 Probalo: Ejecutá el script y presioná Ctrl+C para activar SIGINT.

3. Usá una Queue para que el hilo principal envíe mensajes de "interrupción" o "comando de parada" a los demás hilos.
📁 Carpeta: practica_signals_apunte
    - Archivo: 15_queue_comunicacion.py

4. Simulá un sistema con múltiples hilos que ejecutan tareas críticas. Solo uno debe actuar ante una señal (ej: parar un motor, enviar un log) y los demás deben seguir trabajando hasta recibir orden.
📁 Carpeta: practica_signals_apunte
    - Archivo: 16_accion_critica_un_solo_hilo.py

### 5. Preguntas
1. ¿Qué hilo puede recibir señales en un programa Python multihilo?
Solo el hilo principal del programa puede recibir y manejar señales como SIGINT, SIGTERM, etc.
Los otros hilos no tienen acceso directo al mecanismo de señales del sistema operativo.

🔎 Esto se debe a que el módulo signal de Python está restringido al hilo principal por razones de seguridad y simplicidad del intérprete.

2. ¿Cómo se comunican los hilos cuando se recibe una señal?
Usando mecanismos seguros para múltiples hilos, como:
    - **threading.Event()**: permite activar una señal compartida (como un "flag").
    - **Queue**: permite enviar mensajes o comandos entre hilos.
    - Variables compartidas con locks (aunque menos recomendable para este uso).

🧠 La señal es detectada por el hilo principal, que luego comunica el estado a los demás hilos con esos mecanismos.

3. ¿Qué ventaja ofrece threading.Event() sobre una variable booleana compartida?
threading.Event() es thread-safe: su estado se puede consultar o modificar desde varios hilos sin condiciones de carrera.

🟨 En cambio, una variable booleana global podría modificarse simultáneamente desde varios hilos, lo cual puede causar errores o comportamientos inesperados si no se protege con un lock.

## ✅ Tema 6: Comparación de Señales con Otros Mecanismos de IPC
### 1. 📚 Explicación conceptual
IPC (Inter-Process Communication) significa comunicación entre procesos. Los sistemas operativos ofrecen distintos mecanismos para que los procesos puedan:
    - Coordinarse
    - Compartir datos
    - O enviarse eventos o comandos

Las señales son solo uno de estos mecanismos.

#### Comparación entre mecanismos de IPC (Inter-Process Communication)
1. Señales
    - **¿Qué es?**: Notificaciones asincrónicas que el sistema operativo envía a los procesos.
    - **Uso típico**: Detener, pausar o finalizar procesos.
    - **Ventajas**: Son livianas y se entregan de forma inmediata.
    - **Limitaciones**: Solo permiten enviar eventos simples, sin datos adjuntos.

2. Pipes
    - **¿Qué es?**: Un canal de comunicación unidireccional entre procesos, similar a un archivo.
    - **Uso típico**: Comunicación entre procesos padre e hijo.
    - **Ventajas**: Son sencillos de implementar y útiles en scripts.
    - **Limitaciones**: Solo funcionan entre procesos que están relacionados (por ejemplo, padre-hijo).

3. Sockets
    - **¿Qué es?**: Mecanismo de comunicación que permite enviar datos entre procesos locales o en red.
    - **Uso típico**: Comunicación entre servicios distribuidos o microservicios.
    - **Ventajas**: Muy flexibles; funcionan tanto a nivel local como en red (TCP/UDP).
    - **Limitaciones**: Requieren programación más compleja y control de errores.

4. Shared Memory (Memoria compartida)
    - **¿Qué es?**: Segmento de memoria accesible simultáneamente por varios procesos.
    - **Uso típico**: Transferencia de grandes volúmenes de datos a alta velocidad.
    - **Ventajas**: Es extremadamente rápida y eficiente.
    - **Limitaciones**: Es necesario implementar mecanismos de sincronización como mutexes o semáforos para evitar condiciones de carrera.

5. Message Queues (Colas de mensajes)
    - **¿Qué es?**: Estructura que permite a los procesos intercambiar mensajes con formato estructurado.
    - **Uso típico**: Sistemas distribuidos o aplicaciones en tiempo real.
    - **Ventajas**: Permiten enviar mensajes complejos y conservar el orden de envío.
    - **Limitaciones**: Su uso requiere configuración adicional y administración de la cola.

### 2. 📎 ¿Por qué usar señales en lugar de otros mecanismos?
✅ Ventajas:
    - Simples para eventos como interrupciones (SIGINT), paradas (SIGTERM), alarmas (SIGALRM).
    - No requieren configuración previa entre procesos.
    - Rápidas, gestionadas por el kernel.

❌ Limitaciones:
    - No pueden llevar datos (excepto señales de tiempo real en POSIX).
    - No garantizan orden ni confirmación.
    - Riesgo de errores si no se manejan bien (ej: SIGSEGV mal atrapado).

### 3. 🧪 Ejercicio práctico de comparación
📁 Carpeta: practica_signals_apunte
    - Archivo: 17_comparacion_ipc.py

### 4. Preguntas
1. ¿Qué ventajas tienen las señales respecto a otros métodos como sockets o pipes?
Las señales tienen varias ventajas importantes frente a otros mecanismos como sockets o pipes:
    - Simplicidad: No requieren establecer una conexión ni estructuras previas. Basta con conocer el PID del proceso y usar kill() o os.kill() en Python.
    - Rapidez: Como están gestionadas directamente por el núcleo del sistema operativo, la entrega suele ser inmediata.
    - Bajo consumo de recursos: No ocupan espacio en memoria ni generan buffers de datos como en pipes o sockets.
    - Ideales para eventos simples: Son perfectas para tareas como finalizar (SIGTERM), interrumpir (SIGINT) o reiniciar (SIGHUP) procesos.

🔎 En resumen, las señales son útiles cuando querés avisar o controlar un proceso con una instrucción simple, sin necesidad de transmitir datos complejos.

2. ¿Cuándo NO conviene usar señales?
No conviene usar señales en las siguientes situaciones:
    - Cuando se necesita enviar datos: Las señales tradicionales no permiten enviar información adicional (salvo algunas señales de tiempo real en POSIX).
    -En protocolos complejos: Si necesitás que los procesos intercambien estructuras de datos o mantengan un estado compartido, es mejor usar pipes, sockets o memoria compartida.
    - En aplicaciones críticas: Las señales interrumpen el flujo del programa, lo cual puede provocar condiciones de carrera si no se manejan correctamente (especialmente en programas multihilo).
    - Si necesitás asegurar el orden: Las señales no garantizan orden de entrega ni recepción confiable. Si enviás varias, puede que alguna se pierda.

🔒 Por eso, en sistemas donde la confiabilidad y la estructura del mensaje son importantes, se prefiere usar mecanismos como sockets o colas de mensajes.

3. ¿Qué diferencia práctica observaste entre enviar una señal y pasar un mensaje por pipe?
Enviar una señal:
    - Solo avisa que algo pasó (como una interrupción), sin contenido adicional.
    - Es manejada por una función (signal handler) previamente registrada.
    - Se entrega inmediatamente al proceso.
    - Solo el proceso puede decidir cómo reaccionar, no hay un "mensaje" como tal.

Usar un pipe:
    - Permite enviar datos concretos (cadenas, números, etc.).
    - Requiere lectura y escritura explícita (como en archivos).
    - Es sincrónico o bloqueante (el proceso puede esperar datos).
    - Permite comunicación bidireccional si se configura así.

🎯 En resumen:
    - **Señales**: eventos rápidos, sin datos.
    - **Pipes**: mensajes más ricos, pero requieren coordinación.