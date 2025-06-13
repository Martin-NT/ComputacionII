## Ejercicio 1: Creación de Procesos con Argumentos

Escriba un script en Python llamado `gestor.py` que reciba argumentos desde la línea de comandos utilizando `argparse`:

- La opción `--num` indica la cantidad de procesos hijos a crear.
- La opción `--verbose` activa mensajes detallados.

Cada proceso hijo debe dormir entre 1 y 5 segundos y luego terminar. El proceso padre debe imprimir su PID y mostrar la jerarquía de procesos usando `pstree -p`.

Desde otra terminal, el estudiante deberá observar el estado de los procesos con `ps` o accediendo a `/proc`.

## 🧪 ¿Cómo probarlo?
### 1. Ejecutar el script desde una terminal:
```bash
python3 gestor.py --num <cantidad_de_hijos> --verbose
```
Ejemplo
```bash
python3 gestor.py --num 3 --verbose
```
Esto:
- Crea 3 procesos hijos.
- Cada uno duerme entre 1 y 5 segundos.
- Imprime mensajes detallados si --verbose está activado.
- Muestra la jerarquía de procesos usando pstree -p.

### 2. Desde otra terminal:
```bash
cat /proc/<pid>/status
```
También podés explorar el estado de los procesos en /proc:También podés explorar el estado de los procesos en /proc:
```bash
ps -f --ppid <PID_DEL_PADRE>
```
## 🧠 Conceptos Clave
- multiprocessing.Process: permite crear procesos separados (no hilos).
- os.getpid() / os.getppid(): devuelven el ID del proceso actual y su padre.
- subprocess.run(["pstree", "-p", str(os.getpid())]): ejecuta un comando externo y muestra la jerarquía de procesos.