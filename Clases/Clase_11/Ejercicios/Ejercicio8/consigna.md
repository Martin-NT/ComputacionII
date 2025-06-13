## Ejercicio 8: Condición de Carrera y su Corrección

Implemente un contador compartido entre dos procesos sin usar `Lock`, para evidenciar una condición de carrera. Luego modifique el programa para corregir el problema usando `multiprocessing.Lock`.

Compare ambos resultados.

---

## 🧠 ¿Qué es una condición de carrera?
Es cuando varios procesos o hilos acceden al mismo recurso (como una variable) al mismo tiempo sin coordinación, y eso lleva a resultados incorrectos o inconsistentes.

## 📋 Parte 1 — SIN Lock (con error por condición de carrera)
- Código: contador_sin_lock.py

### 🔍 ¿Qué esperás?
- Cada proceso suma 100000 → el resultado correcto sería 200000.
- Pero como ambos acceden al mismo tiempo sin coordinarse, el valor será menor (¡condición de carrera!).

## 📋 Parte 2 — CON Lock (solución correcta)
- Código: contador_con_lock.py

## 🧪 ¿Cómo ejecutar y comparar?
1. Ejecutá primero sin Lock:
```bash
python3 contador_sin_lock.py
```
🔴 El valor suele estar por debajo de 200000

2. Luego ejecutá con Lock:
```bash
python3 contador_con_lock.py
```
✅ Verás el valor correcto 200000