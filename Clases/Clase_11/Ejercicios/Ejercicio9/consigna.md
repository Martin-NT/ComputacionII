## Ejercicio 9: Control de concurrencia con `Semaphore`

Implemente una versión del problema de los "puestos limitados" usando `multiprocessing.Semaphore`. Cree 10 procesos que intenten acceder a una zona crítica que solo permite 3 accesos simultáneos.

---

## 🧠 Objetivo del ejercicio
Simular una situación donde:
- Hay 10 procesos que quieren acceder a una "zona crítica" (por ejemplo, puestos de trabajo).
- Solo 3 pueden estar dentro al mismo tiempo.
- Los demás deben esperar hasta que haya lugar libre.
- Se usa multiprocessing.Semaphore(3) para controlar esto.

## 🧪 ¿Cómo probarlo?
1. Ejecuta en la terminal:
```bash
python3 ejercicio9.py
```
✅ Como máximo verás 3 procesos "ENTRÓ al puesto" al mismo tiempo. Los demás esperan hasta que alguien salga.

## 🧠 ¿Por qué usar un Semaphore?
A diferencia de un Lock (que permite solo 1 proceso), el Semaphore(n) permite hasta n procesos simultáneamente.
Es ideal para controlar recursos limitados y compartidos, como:
    - Cabinas de teléfono
    - Impresoras
    - Licencias de software
