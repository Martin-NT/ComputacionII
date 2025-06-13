## Ejercicio 11: Manejo de Señales

Cree un script que instale un manejador para la señal `SIGUSR1`. El proceso deberá estar en espera pasiva (`pause()` o bucle infinito).

Desde Bash, envíe la señal al proceso con `kill -SIGUSR1 [pid]` y verifique la respuesta.

---
## 🧠 Objetivo del ejercicio
- Crear un script que espere pasivamente.
- Instalar un manejador de señal para SIGUSR1.
- Cuando reciba la señal, mostrar un mensaje.
- Enviar la señal manualmente con kill.

## 🧪 Cómo probarlo paso a paso
1. Ejecutá el script en una terminal:
```bash
python3 ejercicio11.py
```
Verás algo como:
```bash
Proceso PID: 45012
Esperando señal SIGUSR1...

```

2. Abrí otra terminal y enviá la señal:
```bash
kill -SIGUSR1 45012
```
Sustituyendo 45012 por el PID real que te muestra el programa
```bash
kill -SIGUSR1 <PID>
```
El proceso sigue corriendo después de manejar la señal.

## 📌 Notas importantes
| Punto                    | Detalle                                                   |
| ------------------------ | --------------------------------------------------------- |
| `signal.signal(...)`     | Asigna una función al evento `SIGUSR1`.                   |
| `SIGUSR1`                | Es una señal definida por el usuario.                     |
| `time.sleep(1)` en bucle | Mantiene el proceso vivo sin usar `pause()` directamente. |
| `kill -SIGUSR1 [PID]`    | Enviás la señal al proceso desde otra terminal.           |
