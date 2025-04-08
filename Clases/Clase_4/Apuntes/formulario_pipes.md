# 📝 Formulario: Pipes y Comunicación entre Procesos en Sistemas UNIX/Linux

---

## Pregunta 1  
**Doug McIlroy, al proponer la idea de los pipes, estaba abordando un problema específico en los sistemas de la época. ¿Cuál era ese problema fundamental que los pipes resolvieron?**  
*(2 puntos)*

- [x] **La ineficiencia en términos de almacenamiento y rendimiento debido al uso de archivos temporales para la comunicación entre procesos** ✅  
- [ ] La excesiva complejidad de la programación paralela en los primeros sistemas multiprocesador  
- [ ] La imposibilidad de redireccionar la salida estándar de los programas en las primeras shells de UNIX  

**Justificación:**  
Antes de los pipes, los procesos intercambiaban datos usando archivos temporales, lo cual era lento y costoso en términos de I/O y almacenamiento. Los pipes resolvieron esto con comunicación directa en memoria.

---

## Pregunta 2  
**Cuando un proceso escribe en un pipe lleno mientras simultáneamente espera leer datos de otro pipe que no puede ser escrito porque otros procesos están bloqueados, se produce un escenario conocido como:**  
*(2 puntos)*

- [ ] Ciclo del pipe lleno (pipe full cycle)  
- [ ] Inanición de recursos (resource starvation)  
- [x] **Problema del escritor perezoso (lazy writer problem)** ✅  

**Justificación:**  
Este escenario es un ejemplo clásico de **"problema del escritor perezoso"**, donde procesos quedan bloqueados por no cerrar adecuadamente los extremos del pipe o esperar escrituras que no pueden ocurrir, causando un bloqueo circular.

---

## Pregunta 3  
**En el contexto de los pipes en sistemas UNIX/Linux, ¿cuál de las siguientes afirmaciones explica mejor por qué es crucial cerrar los extremos no utilizados de un pipe después de una llamada a fork()?**  
*(2 puntos)*

- [ ] Para liberar recursos del sistema, ya que cada descriptor de archivo abierto consume memoria del kernel  
- [x] **Para permitir la señalización correcta de EOF, ya que un proceso lector solo recibirá EOF cuando todos los descriptores de escritura hayan sido cerrados** ✅  
- [ ] Para mejorar el rendimiento, ya que los pipes con múltiples descriptores abiertos son significativamente más lentos  

**Justificación:**  
Cerrar los extremos no usados es crucial para que el proceso lector pueda detectar el fin de la transmisión de datos (EOF). Si un descriptor de escritura permanece abierto, el lector quedará esperando indefinidamente.

---

## Pregunta 4  
**En la implementación interna de los pipes en sistemas tipo UNIX, el componente que permite una utilización eficiente del espacio al facilitar que los datos "envuelvan" alrededor de sus límites es:**  
*(2 puntos)*

- [ ] El mecanismo de sincronización de semáforos  
- [ ] Los contadores y flags de estado  
- [x] **El buffer circular** ✅  

**Justificación:**  
Los pipes usan un **buffer circular**, que permite reutilizar el espacio de manera continua, "envolviendo" el puntero de escritura al principio del buffer cuando se alcanza el final, maximizando el uso eficiente de la memoria.

---

## Pregunta 5  
**Cuando se implementa un patrón pipeline de procesamiento con múltiples procesos conectados por pipes, ¿cuál de los siguientes factores representa la limitación o desventaja más significativa inherente a este diseño?**  
*(2 puntos)*

- [ ] La integridad de los datos puede verse comprometida debido a la naturaleza asíncrona de la comunicación  
- [x] **La tasa de procesamiento global está limitada por el proceso más lento en la cadena, lo que se conoce como "tasa de goteo" (drip rate)** ✅  
- [ ] La complejidad algorítmica aumenta exponencialmente con cada proceso adicional en el pipeline  

**Justificación:**  
En un pipeline, la **tasa de procesamiento global** está limitada por el proceso más lento, generando un "cuello de botella". Esta limitación natural se denomina **drip rate** y afecta el throughput general del sistema.

---

