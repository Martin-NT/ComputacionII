## Ejercicio 20: Interacción entre Procesos con Señales Personalizadas

Implemente dos scripts: uno que espera indefinidamente (`pause`) y otro que envía señales (`SIGUSR1`, `SIGUSR2`) cada cierto tiempo. El receptor deberá reaccionar de forma distinta según la señal recibida.

---
## 🧪 ¿Cómo probarlo?
1. Ejecute desde la terminal 1:
```bash
python3 receptor.py
```
- Anotá el PID que imprime.

2. Ejecute desde la terminal 2:
```bash
python3 emisor.py <PID_receptor>
```
- Reemplazando <PID_receptor> con el número que anotaste.

3. Observá cómo el receptor imprime mensajes distintos según la señal recibida.