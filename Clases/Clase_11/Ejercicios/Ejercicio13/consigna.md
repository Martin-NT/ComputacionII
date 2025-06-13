## Ejercicio 13: Visualización de Jerarquía de Procesos

Ejecute un script en Python que cree dos procesos hijos. Desde Bash, utilice `pstree -p` y `ps --forest` para observar la jerarquía. Capture la salida y explique la genealogía de los procesos.

---

## 🧠 Objetivo
- Crear un script Python que lance 2 procesos hijos.
- Observar la jerarquía de procesos con herramientas del sistema.
- Explicar cómo se relacionan.

## 🧪 Cómo ejecutarlo paso a paso
1. Ejecutá el script en una terminal:
```bash
python3 ejercicio13.py
```

2. En otra terminal, usá:
```bash
pstree -p
pstree -p | grep -A 5 python3

```
y observá la jerarquía de procesos, buscando los procesos python3.

3. Luego ejecuta en la misma terminal:
```bash
ps --forest
ps --forest <PPID>

```
y también buscá los procesos python3 para ver la genealogía.



## ✅ ¿Qué muestra esto?
1. Ejecución y salida en Terminal 1
```bash
Padre PID 61604 creando hijos...
Hijo PID 61605 | Padre PID 61604
Hijo PID 61606 | Padre PID 61604
```
Esta salida indica que:
- El proceso padre tiene PID 61604.
- Se crearon dos hijos con PIDs 61605 y 61606, y ambos tienen como padre al proceso 61604.

2. Inspección de la jerarquía de procesos desde Terminal 2
- Comando pstree -p | grep -A 5 python3
```bash
           |               |-gnome-terminal-(45805)-+-zsh(48768)-+-python3(60617)-+-python3(60618)
           |               |                        |            |                `-python3(60619)
           |               |                        |            |-python3(61429)-+-python3(61430)
           |               |                        |            `-python3(61604)-+-python3(61605)
           |               |                        |                             `-python3(61606)
           |               |                        |-zsh(54474)-+-grep(61625)
           |               |                        |            `-pstree(61624)
           |               |                        |-{gnome-terminal-}(45807)

```
Esta salida muestra en forma gráfica la genealogía de procesos:
- El proceso python3(61604) es el padre que ejecutó el script.
- Sus hijos son los procesos python3(61605) y python3(61606), que aparecen conectados justo debajo del padre.

- Comando ps --forest 61604
```bash
    PID TTY      STAT   TIME COMMAND
  61604 pts/2    S+     0:00 python3 ejercicio13.py
```
Este comando muestra el proceso con PID 61604, que es el padre, y dado que los hijos ya finalizaron o no están visibles en ese instante, sólo aparece el padre. Si se ejecuta durante el time.sleep(20) de los hijos, deberían verse también los procesos hijos debajo del padre en forma de árbol.

## Explicación general de la genealogía de procesos
- Cuando ejecutamos un script con multiprocessing en Python, el proceso principal (padre) crea nuevos procesos hijos que son independientes en cuanto a ejecución pero mantienen una relación padre-hijo visible a nivel del sistema operativo.

- Cada proceso tiene un identificador único (PID) y un identificador de proceso padre (PPID).

- El comando pstree muestra la jerarquía de procesos en forma de árbol, permitiendo visualizar qué procesos fueron creados por quién.

- ps --forest también permite ver la jerarquía pero con más detalle sobre estado y terminal asociado.

- En este ejercicio se confirma que los procesos hijos (python3 hijos) están correctamente vinculados al padre, ya que su PPID coincide con el PID del padre.

- El mantener los hijos con sleep los mantiene activos para poder inspeccionarlos con estos comandos.

- Cuando los hijos finalizan, desaparecen de la lista de procesos.

## 🧠 ¿Qué aprendés?
| Herramienta    | Qué muestra                        |
| -------------- | ---------------------------------- |
| `pstree -p`    | Jerarquía gráfica de procesos      |
| `ps --forest`  | Árbol textual de procesos y padres |
| `os.getpid()`  | PID del proceso actual             |
| `os.getppid()` | PID del proceso padre              |
