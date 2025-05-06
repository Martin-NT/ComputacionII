# Sección 1: ¿Qué es un FIFO y por qué se usa?
## 🧠 Teoría: Comunicación entre Procesos con FIFOs
Un FIFO (First-In-First-Out), también conocido como named pipe, es un archivo especial que permite la comunicación entre procesos (IPC). A diferencia de los pipes anónimos, que solo sirven entre procesos relacionados (por ejemplo, padre e hijo), los FIFOs son persistentes y están ubicados en el sistema de archivos. Esto significa que cualquier proceso que tenga los permisos necesarios puede abrir el FIFO y comunicarse.

### Características clave:

- FIFO significa que el primer dato que entra, es el primero que sale.
- Los FIFOs persisten como archivos en el sistema hasta que los elimines.
- Son unidireccionales por defecto, pero se pueden usar en pares para comunicación bidireccional.
- Si un proceso intenta leer un FIFO sin que nadie lo haya abierto para escribir, se bloquea (salvo que use O_NONBLOCK).


## 🧪 Práctica: Crear un FIFO en el sistema
### Crear un FIFO en Linux
Desde la terminal:
mkfifo /tmp/mi_fifo

Este comando crea un archivo especial en /tmp. Podés verificarlo con:
ls -l /tmp/mi_fifo

Deberías ver algo como:
prw-r--r-- 1 tu_usuario tu_grupo 0 fecha /tmp/mi_fifo

### Ejemplo Practico: Escritura y lectura desde FIFO
📁 Carpeta: escritura_lectura_fifo
Archivos:
- escribir_fifo.py
- leer_fifo.py

## Preguntas
1. ¿Cuál es la principal diferencia entre un FIFO y un pipe anónimo?
✅ Respuesta:
La diferencia principal es que el FIFO es persistente y visible en el sistema de archivos, mientras que el pipe anónimo es temporal y sólo funciona entre procesos relacionados (por ejemplo, padre e hijo).

Explicación:
Un pipe anónimo se crea en tiempo de ejecución (por ejemplo, con os.pipe() en Python) y no tiene nombre. Sólo pueden usarlo procesos que comparten herencia del descriptor (por ejemplo, después de un fork()).

Un FIFO se crea como un archivo especial con mkfifo, y puede ser usado por cualquier proceso, en cualquier momento, siempre que tenga permisos y sepa el nombre del archivo.

Ejemplo práctico:
Con un FIFO en /tmp/mi_fifo, podés tener dos scripts independientes en distintas carpetas, y aún así pueden comunicarse a través de ese archivo.

2. ¿Qué pasa si abrís un FIFO para lectura y nadie lo ha abierto aún para escritura?
✅ Respuesta:
El proceso que intenta leer queda bloqueado: se queda esperando hasta que otro proceso abra el FIFO para escritura.

Explicación:
Esto es una medida de sincronización automática. Si no hubiera nadie escribiendo, no tendría sentido que el lector reciba datos. Por eso, el kernel lo pone en pausa hasta que haya alguien escribiendo.

⚠️ Podés evitar ese bloqueo usando la bandera O_NONBLOCK, pero entonces tendrás que manejar vos el error o la falta de datos.

3. ¿Por qué es útil que el FIFO esté en el sistema de archivos?
✅ Respuesta:
Porque eso permite que procesos completamente independientes se comuniquen sin necesidad de compartir herencia, archivos temporales o estructuras especiales.

Explicación:
Un FIFO se comporta como un archivo, pero su contenido no se guarda: los datos pasan por él como un tubo. Al estar en el sistema de archivos, podés:

- Supervisarlo (ls, stat)
- Protegerlo con permisos
- Usarlo desde cualquier lenguaje o proceso

Esto permite construir sistemas más modulares, como por ejemplo:

- Un logger central que recibe datos de varios procesos.
- Un canal de eventos entre scripts en Bash, Python, etc.

# 🧠 Lectura no bloqueante y posición del cursor en FIFOs
## 1. Teoría: Lectura no bloqueante (O_NONBLOCK)
Cuando un proceso abre un FIFO para lectura, normalmente:

- Se bloquea si aún no hay ningún escritor.
- Y luego espera si no hay datos disponibles en el buffer.

Pero si lo abrís con la flag O_NONBLOCK, el proceso:

- No se bloquea nunca.
- En lugar de quedarse esperando, devuelve un error o una lectura vacía si no hay datos.

✅ Esto es útil en programas que no pueden detenerse, como demonios, servidores o multiplexores que monitorean muchos FIFOs al mismo tiempo.

## 2. Teoría: Posición del cursor (y comportamiento destructivo)
Este punto es clave: en un FIFO, los datos se consumen al leerlos.

🔁 Eso significa que:

- El primer lector recibe los primeros datos (por ejemplo, los primeros 3 bytes).
- Otro lector, aunque tenga su propio descriptor, ya no podrá volver a leerlos.
- El cursor es compartido a nivel de buffer, no a nivel de descriptor de archivo como en los archivos normales.

🧪 Esto permite demostrar que dos procesos leyendo el mismo FIFO no ven lo mismo si no se coordinan.

## Ejemplo práctico: Lectura no compartida
📁 Carpeta: lectura_no_compartida
Archivos: 
- escribir_fifo_cursor.py
- lector_1.py
- lector_2.py
### Paso 1: Crear el FIFO
Desde la terminal:
mkfifo /tmp/fifo_cursor

### Paso 2: Ejecuta script para escribir
python3 escribir_fifo_cursor.py

### Paso 3: Ejecuta primer lector 
python3 lector_1.py

### Paso 4: Ejecuta segundo lector
python3 lector_2.py

Los primeros 3 bytes ya no están disponibles para el segundo lector.

### 🔍 ¿Por qué en la terminal 3 (lector_2) "no pasa nada"?
Esto ocurre porque:
- Los datos ya fueron consumidos por lector_1.py.
- Como los FIFOs no almacenan los datos una vez leídos, cuando lector_2.py intenta leer, el FIFO está vacío.
- Si no hay más datos en el buffer y el lector no usa modo no bloqueante (O_NONBLOCK), entonces queda bloqueado esperando datos nuevos que nunca llegan.

## Preguntas
1. ¿Qué hace O_NONBLOCK cuando abrís un FIFO?
✅ O_NONBLOCK le indica al sistema que no debe bloquear al proceso si el otro extremo del FIFO no está listo o si no hay datos disponibles.

O_NONBLOCK evita que el proceso quede bloqueado al abrir o leer un FIFO.
- Si no hay un escritor presente al abrirlo, lanza un error en lugar de esperar.
- Si no hay datos disponibles al leer, devuelve inmediatamente sin bloquear.

2. ¿Los datos leídos de un FIFO pueden volver a leerse por otro proceso?
✅ No, los datos en un FIFO se consumen al leerlos. Una vez que un proceso los lee, ya no están disponibles para otros procesos, incluso si estos abren el FIFO después.

👉 Esto se llama comportamiento destructivo y secuencial, a diferencia de un archivo normal que podés leer varias veces.

3. ¿Qué pasa si dos procesos leen el mismo FIFO al mismo tiempo?
✅ Uno de los procesos lee los datos primero. El segundo puede recibir el resto, o nada si el primero ya vació el FIFO.

# 🛠️ Implementación de un sistema de log con FIFO en Python
## 🎓 1. 📖 Concepto teórico
Un sistema de log permite que múltiples procesos envíen mensajes a un proceso central que los guarda en un archivo. Con un FIFO, podemos conectar esos procesos sin que estén relacionados entre sí.

¿Por qué usar FIFO para logs?
- No necesitamos que los procesos estén emparentados.
- Podemos ver los logs en tiempo real.
- Podemos escribir en el log desde distintos scripts.

Este modelo se llama productor-consumidor:
    - 🟦 El productor (escritor) manda mensajes.
    - 🟨 El consumidor (logger) los recibe y los guarda.


## 🧪 2. Pasos prácticos
📁 Carpeta: logger_fifo
Archivos: 
- logger.py 
Este script lee del FIFO y escribe en un archivo real de log (registro.log).
- escritor.py
Este script envía un mensaje al logger a través del FIFO.

### Paso 1: Crear el FIFO para logging
mkfifo /tmp/log_fifo
    Esto crea un archivo especial donde los procesos pueden escribir mensajes.

### Paso 2: Ejecutar el proceso logger (lector)
1. Abrí una terminal y ejecutá el logger:
python3 logger.py

### Paso 3: Ejecutar el proceso escritor (productor)
2. En otra terminal, ejecutá varias veces el escritor:
python3 escritor.py
📌 Verás que cada mensaje aparece por pantalla y se guarda en el archivo registro.log.

## Preguntas
1. ¿Qué función tiene el proceso logger.py en este sistema?
✅ El logger.py lee del FIFO y guarda los mensajes en un archivo (registro.log).
👉 Es el consumidor en el patrón productor-consumidor.

2. ¿Qué pasa si ejecutás escritor.py y el logger aún no está corriendo?
✅ Si el lector aún no abrió el FIFO, el escritor queda bloqueado esperando que alguien lo abra para lectura.
⚠️ El proceso no falla, pero se detiene hasta que haya un lector.
Si quisieras evitar esa espera, deberías usar os.O_NONBLOCK en lugar de open().

3. ¿Qué ventaja tiene usar un FIFO en lugar de un archivo de texto compartido?
✅  "Mejor control de concurrencia y sincronización en la escritura del log."

Te lo explico:
📁 Si dos procesos escriben directamente en el mismo archivo de texto, pueden pisarse entre sí, corromper el archivo o mezclar líneas.
🧵 En cambio, usando un FIFO como intermediario:
- Cada proceso escribe en el FIFO (uno a la vez, ordenado).
- El logger.py es el único que accede al archivo físico.
- Esto evita conflictos de concurrencia.

# 🛠️ Implementación de un canal de chat usando FIFO en Python
## 🎓 1. 📖 Concepto teórico
Un canal de chat es un ejemplo clásico de comunicación bidireccional entre dos procesos, usando FIFO para enviar y recibir mensajes. A diferencia de un sistema de logs, donde los mensajes solo van en una dirección, un canal de chat requiere que ambos procesos puedan leer y escribir mensajes.

En este caso, vamos a crear dos FIFOs:
- Uno para enviar mensajes de un proceso a otro.
- Otro para la respuesta del segundo proceso.

## 🧪 2. Pasos prácticos
📁 Carpeta: comunicacion_fifo
Archivos: 
- emisor.py
El emisor escribe mensajes en /tmp/chat_in y espera la respuesta en /tmp/chat_out.
- receptor.py
El receptor lee desde /tmp/chat_in y responde en /tmp/chat_out.

### Paso 1: Crear los FIFOs para chat
En la terminal, ejecutá lo siguiente para crear los dos FIFOs:
mkfifo /tmp/chat_in
mkfifo /tmp/chat_out

### Paso 2: Ejecutar el proceso receptor (lector)
python3 receptor.py

### Paso 3: Ejecutar el proceso emisor (escritor)
python3 emisor.py

💬 Ahora podrás escribir y recibir mensajes entre las dos terminales.

## Preguntas
1. ¿Qué función tienen los dos FIFOs (chat_in y chat_out) en este ejemplo?
- El FIFO chat_in es utilizado por el emisor para enviar mensajes al receptor.
- El FIFO chat_out es utilizado por el receptor para enviar una respuesta al emisor.

2. ¿Qué pasa si el proceso receptor no está corriendo cuando el emisor intenta escribir un mensaje?
✅ El emisor quedará bloqueado esperando que el receptor lea el mensaje. Esto se debe a que el FIFO está vacío, y el proceso emisor está esperando que alguien esté listo para leerlo. En otras palabras, si el receptor no está corriendo, el emisor no podrá continuar y quedará esperando en el FIFO.

3. ¿Cuál es la ventaja de usar FIFOs para este canal de chat frente a otras alternativas como sockets?
Ventaja de los FIFOs:

- Simplicidad: Los FIFOs son más simples de implementar que los sockets, especialmente cuando no se necesita comunicación en red. Son directos y se integran de manera natural en el sistema de archivos.

- Sin necesidad de redes: A diferencia de los sockets, que pueden ser utilizados en redes distribuidas, los FIFOs funcionan bien para comunicación local en un solo sistema.

- Interacción con archivos del sistema: Los FIFOs son archivos, por lo que se pueden gestionar usando comandos estándar de Unix, como ls, rm, etc. Son fáciles de depurar y gestionar en la terminal.

Desventajas de los FIFOs:

- Los sockets son más potentes si se necesita comunicación en red o una mayor flexibilidad en la comunicación (por ejemplo, soporte para múltiples clientes, no bloqueante, etc.).

## 📝 Ejercicio Práctico: Implementación de un sistema de log usando FIFO
En este ejercicio, vamos a crear un sistema de logging en el que un proceso productor (logger) escribirá mensajes en un FIFO, y un proceso consumidor (lector) leerá esos mensajes para escribirlos en un archivo de log.

### 🎯 Objetivo:
- Crear dos procesos: un logger y un lector.
- El logger escribirá mensajes en un FIFO.
- El lector leerá esos mensajes y los guardará en un archivo de log.

### 🧪 Pasos Prácticos
📁 Carpeta: log_fifo_system
Archivos: 
- logger_ep.py
Este script escribirá mensajes de log en el FIFO.
- lector_ep.py
Este script leerá los mensajes desde el FIFO y los guardará en un archivo de log.

#### Paso 1: Crear el FIFO para los logs
Primero, en la terminal, creamos el FIFO donde se escribirán los mensajes de log:
mkfifo /tmp/log_fifo

#### Paso 2: Ejecutar el proceso lector (consumidor de logs)
Abre una terminal y ejecuta el lector (consumidor):
python3 lector_ep.py

#### Paso 3: Ejecutar el proceso logger (productor de logs)
Abre otra terminal y ejecuta el logger (productor):
python3 logger_ep.py

El logger pedirá que escribas un mensaje de log. Puedes escribir cualquier mensaje y verlo registrado en el archivo registro.log.

Para finalizar, escribe salir en el logger. El proceso lector continuará hasta que el FIFO se cierre.

## Preguntas
1. ¿Qué hace el comando fifo.flush() en el código del logger?
✅ fifo.flush() fuerza a que los datos escritos con fifo.write() se envíen inmediatamente al FIFO (named pipe), sin esperar a que el búfer se llene.

📌 Ejemplo: Imagina que escribís "Hola" en el FIFO pero no hacés flush(). Ese mensaje podría quedar temporalmente en memoria sin enviarse todavía. Con flush(), asegurás que el lector lo reciba ya.

2. ¿Qué pasa si el lector no está corriendo cuando el logger escribe un mensaje en el FIFO?
✅ Si el FIFO se abre en modo escritura bloqueante (open('/tmp/log_fifo2', 'w')), el proceso se queda esperando hasta que alguien lo abra para lectura.

✅ Si se abre en modo escritura no bloqueante (os.open(..., os.O_WRONLY | os.O_NONBLOCK)), entonces el proceso falla inmediatamente con un error como BrokenPipeError o OSError.

📌 Conclusión: El logger depende de que el lector esté activo. Si no lo está, el logger se bloquea o falla, dependiendo del modo.

3. ¿Cómo se podría mejorar este sistema si tuviéramos muchos mensajes o varios procesos productores de logs?
✅ Aquí hay tres formas de mejorarlo:

- Usar un búfer intermedio o una cola (queue): En lugar de escribir directamente al FIFO, los procesos pueden enviar mensajes a una cola compartida (como una base de datos ligera, Redis o una cola en memoria).

- Usar un FIFO por proceso: Cada logger tiene su propio FIFO. El lector principal lee de todos los FIFOs (por ejemplo, con select o poll) y centraliza los mensajes.

- Cambiar a un sistema más robusto como sockets o colas de mensajes (message queues): Estos mecanismos permiten manejar múltiples clientes, reintentos, y evitan pérdida de mensajes.

📌 Pero recordá: aún no vimos sockets ni colas, así que por ahora lo mejor es practicar con un solo FIFO o usar varios con control manual.

## 🧪 Ejercicio: Múltiples procesos escriben logs a un solo lector
En la carpeta Multiples_procesos
Vamos a implementar:
- ✅ Dos procesos productores (logger1.py, logger2.py)
- ✅ Un proceso lector centralizado (lector_central.py)
- ✅ Un FIFO compartido (/tmp/multilog_fifo)

### 🧠 Concepto clave
Aunque hay múltiples productores, todos escriben al mismo FIFO. Como el FIFO es un canal unidireccional y secuencial, los mensajes se intercalan, pero el lector los recibe en orden de llegada.

### Paso 1: Crear el FIFO
Abrí una terminal y ejecutá:
mkfifo /tmp/multilog_fifo

Si te dice que ya existe, podés ignorar el error o borrarlo con:
rm /tmp/multilog_fifo && mkfifo /tmp/multilog_fifo

### Paso 2: Crear el lector 
lector_central.py

### Paso 3: Crear dos loggers 
logger1.py
logger2.py

### Paso 4: Ejecución paso por paso
1. Terminal 1: Correr el lector
python3 lector_central.py

2. Terminal 2: Correr logger 1
python3 logger1.py

3. Terminal 3: Correr logger 2
python3 logger2.py

Deberías ver algo como:
🔁 Lector central esperando mensajes...
[LOG] Logger 1 - Mensaje 0
[LOG] Logger 2 - Mensaje 0
[LOG] Logger 1 - Mensaje 1
...

## Preguntas
1. ¿Qué mecanismo permite que varios procesos escriban en el mismo FIFO sin corromperse?
✅ El sistema operativo maneja el acceso concurrente al FIFO.

Cuando varios procesos escriben al mismo FIFO, el kernel asegura que cada operación write() sea atómica hasta cierto tamaño (usualmente 4096 bytes en sistemas Linux). Esto significa que si cada proceso escribe menos de ese tamaño por vez (como nuestras líneas de texto), no se mezclan ni se corrompen los datos. Cada mensaje llega completo al lector, aunque el orden depende de quién escribe primero.

2. ¿Qué pasa si logger1 y logger2 escriben al mismo tiempo?
🔄 El FIFO entrega los mensajes en el orden en que llegan al buffer del kernel.

Aunque ambos procesos pueden escribir "al mismo tiempo", el sistema operativo los intercalará según el orden en que sus datos llegaron al FIFO. Así que el lector central los leerá mezclados, pero sin errores:
Ejemplo:
[LOG] Logger 1 - Mensaje 1
[LOG] Logger 2 - Mensaje 1
[LOG] Logger 1 - Mensaje 2
...
El orden puede variar en cada ejecución, dependiendo de la carga del sistema o los sleep().

3. ¿Qué pasaría si logger1 no hiciera .flush()?
🚨 El mensaje podría no llegar al lector inmediatamente o nunca aparecer.

En Python, cuando abrís un archivo o FIFO en modo texto, las escrituras están bufferizadas: es decir, Python espera a juntar varios datos antes de enviarlos todos juntos al sistema operativo. Si no hacés .flush() o no cerrás el archivo (with lo hace automáticamente), los datos quedan en el buffer interno de Python y no se escriben en el FIFO a tiempo, o incluso se pierden si el proceso finaliza abruptamente.

# 🧩 Tema: Lectura desde múltiples FIFOs (lector centralizado)

## 🎓 Parte teórica
Hasta ahora trabajamos con un solo FIFO compartido. Ahora vamos a ver una estrategia diferente:

🔁 Cada proceso escritor tiene su propio FIFO (por ejemplo, /tmp/fifo_logger1, /tmp/fifo_logger2).

👂 Un único proceso lector centralizado se encarga de leer todos esos FIFOs, cada uno en su descriptor de archivo.

🧠 Esto es útil para:

- Sistemas donde cada módulo escribe logs por separado.
- Escuchar a múltiples fuentes al mismo tiempo (como canales independientes).

## 🛠️ Parte práctica
En la carpeta Multiples_fifos_con_lector
1. Crear los FIFOs
En la terminal:
mkfifo /tmp/fifo_logger1
mkfifo /tmp/fifo_logger2
Si ya existen, no hay problema. El sistema te lo dirá.

2. Código de los loggers (escritores individuales)
Archivo: logger1.py
Archivo: logger2.py

3. Código del lector centralizado
Archivo: lector_central.py
📌 Nota: usamos select.select() para esperar a que haya algo disponible en alguno de los FIFOs sin bloquear el programa.

4. Ejecución
Terminal 1: python3 lector_central.py
Terminal 2: python3 logger1.py
Terminal 3: python3 logger2.py

## Preguntas
1. ¿Por qué usamos select.select() en lugar de readline() directamente?

Porque select.select() espera de forma eficiente hasta que haya datos disponibles en uno o más FIFOs. Si usaras readline() directamente en cada FIFO, podrías quedarte bloqueado en un FIFO que todavía no tiene datos, y nunca llegar a leer los otros.

🔍 En resumen:
- readline() bloquea el proceso si el FIFO no tiene datos.
- select.select() no bloquea inútilmente: solo lee cuando realmente hay algo para leer, y puede trabajar con muchos FIFOs al mismo tiempo.

2. ¿Qué ventaja tiene este modelo con múltiples FIFOs sobre uno solo?
Este modelo permite que varios procesos productores envíen mensajes al mismo lector central, sin interferirse entre sí.

🔧 Ventajas:
- Cada productor tiene su FIFO privado → evita colisiones de mensajes.
- El lector central puede recibir de muchos a la vez, usando select() para vigilar todos los canales.
- Se escala mejor si más procesos quieren enviar logs o eventos.

3. ¿Qué pasaría si uno de los FIFOs se cierra inesperadamente?
Si un proceso cierra su FIFO de forma abrupta o termina inesperadamente:
- El lector detecta EOF (fin de archivo) en ese FIFO.
- En Python, readline() devuelve una cadena vacía (''), lo que indica que el otro extremo cerró su escritura.
- El lector puede entonces cerrar ese descriptor y eliminarlo del select().

🔐 Esto es importante para evitar errores o ciclos infinitos leyendo de un canal que ya no está en uso.

## Ejemplo 2
Dentro de la carpeta multiples_fifos_select/, vamos a tener al menos:
- lector_multiple.py → el script que usa select para leer múltiples FIFOs.
- escritor1.py → un proceso que escribe al FIFO /tmp/fifo1.
- escritor2.py → otro proceso que escribe al FIFO /tmp/fifo2.
- Un script crear_fifos.py para crear ambos FIFOs fácilmente.

▶️ Cómo ejecutarlo
1. En una terminal, corré:
python3 crear_fifos.py

2. En otra terminal:
python3 lector_multiple.py

3. En dos terminales distintas:
python3 escritor1.py
python3 escritor2.py

### 🔎 ¿Qué hace select.select()?
- Espera hasta que alguno de los FIFOs tenga datos para leer.
- Así evitamos quedarnos "trabados" con un readline() que espera infinitamente.
- Es útil cuando hay varios FIFOs al mismo tiempo, como en un sistema con varios productores.

### 👇 ¿Qué significa cuando os.read() devuelve ""?
- Significa que el otro proceso cerró el FIFO (ya no hay nadie escribiendo).
- En ese caso, el lector:
    - Muestra un mensaje como 🚫 Se cerró el FIFO /tmp/fifo1
    - Cierra ese descriptor
    - Lo elimina del monitoreo

### 🧠 ¿Por qué es útil este modelo?
- Te permite manejar múltiples productores que escriben en distintos FIFOs.
- Si un productor se va, el lector sigue funcionando con los demás.
- Evita errores como BrokenPipeError o que el lector se quede colgado.

## Ejercicio Final: Mini Chat con FIFOs (full-duplex)
Vamos a simular un chat entre dos procesos, cada uno con su propio FIFO para enviar y recibir mensajes (comunicación bidireccional).

📁 Carpeta: chat_fifo
1. crear_fifos.py
2. usuario_a.py — Envía por chat_a_b y recibe por chat_b_a
3. usuario_b.py — Envía por chat_b_a y recibe por chat_a_b

▶️ Cómo usarlo
1. Ejecutá crear_fifos.py una vez:
python3 crear_fifos.py

2. Abrí dos terminales:
- En una: python3 usuario_a.py
- En otra: python3 usuario_b.py
Escribí desde ambos lados y verás que se comunican como en un chat.

## Preguntas
1. ¿Por qué es importante tener un FIFO por cada dirección de comunicación en un chat?
Es importante tener un FIFO para cada dirección de comunicación porque en un chat, cada usuario necesita un canal dedicado para enviar y recibir mensajes. Esto asegura que:

- La comunicación sea independiente: Si usáramos un solo FIFO bidireccional, tanto los mensajes enviados como recibidos podrían mezclarse, causando confusión.

- Evitar interferencias: Si solo tuviéramos un FIFO para ambos mensajes, los mensajes podrían solaparse, y el proceso receptor no sabría si está leyendo un mensaje enviado o una respuesta.

Por eso, en un sistema de chat típico con dos usuarios, se crean dos FIFOs: uno para que cada uno envíe mensajes y otro para que reciba mensajes.

2. ¿Qué ventaja tiene usar hilos (threads) en este último ejercicio?
Usar hilos (threads) tiene varias ventajas, especialmente cuando tratamos con procesos como un chat, que necesitan leer y escribir de manera concurrente. Algunas de las ventajas son:

- Paralelismo: Los hilos permiten ejecutar simultáneamente operaciones de lectura y escritura. Mientras un hilo está esperando la entrada del usuario (o leyendo de un FIFO), el otro hilo puede estar escribiendo en el FIFO o mostrando los mensajes que ha recibido.

- Mejor rendimiento: Sin bloquear el proceso principal, los hilos permiten que ambos procesos se mantengan activos sin que uno tenga que esperar el otro. Esto hace que el chat sea más fluido y eficiente, ya que ambas operaciones (leer y escribir) pueden ocurrir al mismo tiempo.

- Simplificación del código: Usando hilos, podemos hacer que el código sea más claro, sin tener que implementar complicados mecanismos de espera o sincronización entre procesos.

3. ¿Qué pasa si uno de los procesos termina abruptamente?
Si uno de los procesos termina de forma inesperada (por ejemplo, se cierra o tiene un error), esto afectará a la comunicación entre ambos, dependiendo de cómo esté implementada:

- Proceso de lectura: Si el proceso que está leyendo del FIFO termina inesperadamente, el proceso que está escribiendo puede recibir un error como BrokenPipeError (si está intentando escribir en un FIFO cerrado). Esto puede interrumpir el chat y causar que el proceso escritor termine o imprima un mensaje de error.

- Proceso de escritura: Si el proceso que está escribiendo en un FIFO termina inesperadamente, el proceso receptor podría no recibir más mensajes. El receptor puede bloquearse esperando mensajes que nunca llegarán, o recibir un EOF (fin de archivo) si el FIFO se cierra por completo.