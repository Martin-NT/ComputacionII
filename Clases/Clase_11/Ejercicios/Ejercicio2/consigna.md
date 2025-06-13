## Ejercicio 2: Proceso Zombi

Cree un script en Python que genere un proceso hijo que finaliza inmediatamente. El padre no deberá recolectar su estado hasta al menos 10 segundos después.

Desde Bash, utilice `ps` y `/proc/[pid]/status` para identificar el estado Z (zombi) del hijo.

---

## 🧪 ¿Cómo probarlo?
### 1. Desde la terminal 1:
```bash
python3 zombi.py
```

### 2. Desde una segunda terminal, mientras esperás los 10 segundos:
#### a. Ver el proceso como zombi usando ps:
La columna STAT mostrará Z si el proceso es zombi.
```bash
ps -l | grep Z
```
O directamente:
```bash
ps -o pid,ppid,state,cmd -p <pid_del_hijo>
```

#### b. Ver en /proc:
```bash
cat /proc/<pid_del_hijo>/status
```
Y deberías ver:
State:	Z (zombie)

## 🧠 Explicación técnica
- os.fork() crea un nuevo proceso (hijo).
- os._exit(0) hace que el hijo finalice inmediatamente y sin errores.
- El proceso padre no ejecuta waitpid() durante 10 segundos, por lo que el sistema mantiene al hijo como zombi (está muerto, pero su información aún no fue recolectada).
- os.waitpid(pid, 0) finalmente recolecta al hijo, liberando sus recursos.