## Ejercicio 10: Sincronización con `RLock`

Diseñe una clase `CuentaBancaria` con métodos `depositar` y `retirar`, ambos protegidos con un `RLock`. Permita que estos métodos se llamen recursivamente (desde otros métodos sincronizados).

Simule accesos concurrentes desde varios procesos.

---
## 🧠 Objetivo
- Crear una clase CuentaBancaria con saldo compartido.
- Usar un multiprocessing.RLock para sincronizar el acceso al saldo.
- Permitir llamadas recursivas a métodos sincronizados.
- Simular accesos desde múltiples procesos.

## 🧪 ¿Cómo probarlo?
1. Ejecuta desde la terminal:
```bash
python3 ejercicio10.py
```
✅ Todos los accesos al saldo están protegidos, y los métodos anidados (_actualizar_saldo) no bloquean gracias al RLock.

## 🧠 ¿Por qué no usar Lock común?
Si usás multiprocessing.Lock y hacés que un método sincronizado llame a otro con el mismo lock, se bloquearía a sí mismo (deadlock).
Un RLock permite que el mismo proceso adquiera el lock varias veces sin trabarse.