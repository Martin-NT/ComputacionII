## Ejercicio 14: Ejecución Diferida y Sincronización con `sleep`

Cree un script Bash que ejecute en segundo plano un script Python que duerme 10 segundos. Desde otra terminal, verifique su ejecución con `ps`, y envíe una señal para terminarlo prematuramente (`SIGTERM`).

---

Este script:
- Captura la señal SIGTERM para imprimir un mensaje antes de terminar.
- Duerme 10 segundos para simular un trabajo en segundo plano.

## 🧪 Cómo ejecutarlo paso a paso
1. Dale permisos para ejecutar
```bash
chmod +x lanzar.sh
```

2. Abre terminal 1 y ejecuta:
```bash
./lanzar.sh
```

3. Abre terminal 2 y ejecuta para ver el proceso:
```bash
ps -p <PID>
```
Para terminarlo prematuramente (antes de los 10 segundos), en terminal 2 ejecuta:
```bash
kill -SIGTERM <PID>
```

## Explicación
- El script Bash ejecuta el script Python en segundo plano para no bloquear la terminal.
- $! guarda el PID del proceso lanzado en background.
- Desde otra terminal podemos ver si el proceso sigue activo con ps.
- Usando kill -SIGTERM PID podemos enviar una señal para terminar el proceso.
- El script Python simplemente duerme 10 segundos, pero puede ser terminado antes si recibe señal.