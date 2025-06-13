## Ejercicio 4: Reemplazo con `exec()`

Implemente un script que use `fork()` para crear un proceso hijo. Ese hijo deberá reemplazar su imagen de ejecución por el comando `ls -l` usando `exec()`.

Desde Bash, verifique el reemplazo observando el nombre del proceso con `ps`.

---

## Explicación paso a paso:
1. Importamos os para usar fork() y execvp() y sys para salir si hay error.
2. Imprimimos el PID del proceso padre para referencia.
3. Ejecutamos os.fork(), que crea un proceso hijo idéntico.
4. Si pid == 0, estamos en el hijo:
    - Imprimimos su PID.
    - Usamos os.execvp() para reemplazar la imagen del proceso hijo con el programa ls -l.
    - execvp ejecuta el comando y reemplaza el proceso actual (el hijo).
    - Si execvp falla, imprimimos error y salimos.
5. Si pid != 0, estamos en el padre:
    - Imprimimos que esperamos al hijo.
    - Usamos os.wait() para esperar que el hijo termine (el hijo ejecutará ls -l).
    - Luego el padre imprime que el hijo terminó.

- fork(): para crear un nuevo proceso (hijo).
- exec(): para que ese hijo reemplaze su código por un programa externo (como ls -l).
- ps: para ver en terminal qué procesos están corriendo.

## 🧪 ¿Cómo probarlo?
### Ejecuta el script:
```bash
python3 ejercicio4.py
```

### Para verificar el reemplazo del proceso hijo desde otra terminal mientras el script corre, haz lo siguiente rápido después de lanzar el script:
```bash
ps -ef | grep ejercicio4.py
ps -ef | grep sh
ps -ef | grep ls
```
Verás que el proceso hijo deja de ser el script Python y aparece como ls -l mientras se ejecuta.

#### Comando:
```bash
ps -ef | grep ejercicio4.py
```
Esto te dice qué procesos tienen ese nombre en su línea de comando. Por ejemplo:
```bash
martin     33352   18927  7 11:08 pts/3    00:00:00 python3 ejercicio4.py
```
PID 33352 → este es el proceso padre, corriendo tu script Python.
El hijo ya no aparece con ese nombre porque su imagen fue reemplazada por sh.

#### Comando:
```bash
ps -ef | grep sh
```
Este sí te muestra algo clave:
```bash
martin     33353   33352  0 11:08 pts/3    00:00:00 sh -c ls -l; sleep 5
```
Este es el proceso hijo.
Su PID es 33353 (como te lo mostró el script).
Este proceso ejecuta el comando ls -l; sleep 5.

✅ Esto demuestra que el hijo dejó de ser código Python y fue reemplazado por el shell que corre ls y sleep. ¡Exactamente lo que querías hacer!

#### Comando:
```bash
ps -ef | grep ls
```
Esto busca procesos cuyo nombre incluya ls. Pero en tu caso, ls fue ejecutado dentro de un shell (sh), y terminó muy rápido. Por eso, ¡no aparece!