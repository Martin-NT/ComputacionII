## Ejercicio 3: Proceso Huérfano

Diseñe un script que cree un proceso hijo que siga ejecutándose luego de que el proceso padre haya terminado. Verifique desde Bash que el nuevo `PPID` del proceso hijo corresponde a `init` o `systemd`.

---

## 🧪 ¿Cómo probarlo?
### 1. Desde una terminal, ejecutá el script:
```bash
python3 huerfano.py
```

### 2. En otra terminal, antes de que pasen los 40 segundos:
```bash
ps -o pid,ppid,state,cmd -p <PID_DEL_HIJO>
```

### 3. También podés ver el estado desde /proc:
```bash
cat /proc/<PID_DEL_HIJO>/status | grep PPid
```

### 4. Ver quién es ese nuevo padre
```bash
ps -p <PPID_DEL_HIJO> -o pid,cmd
```