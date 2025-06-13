## Ejercicio 12: Ejecución Encadenada con `argparse` y Pipes

Implemente dos scripts:

1. `generador.py`: genera una serie de números aleatorios (parámetro `--n`) y los imprime por salida estándar.
2. `filtro.py`: recibe números por entrada estándar y muestra solo los mayores que un umbral (parámetro `--min`).

Desde Bash, encadene la salida del primero a la entrada del segundo:

```bash
generador.py --n 100 | filtro.py --min 50
```
---

## 📝 1. generador.py: genera números aleatorios
Genera n números aleatorios entre 0 y 100 y los imprime uno por línea.

## 📝 2. filtro.py: filtra según umbral mínimo
Lee números desde stdin, y muestra solo los mayores a --min.

## 🧪 Cómo probarlo
1. Asegurate de que ambos scripts tienen permiso de ejecución:
```bash
chmod +x generador.py filtro.py
```

2. Ejecutá el encadenamiento con un pipe:
```bash
./generador.py --n 100 | ./filtro.py --min 50
```
✅ Verás una lista con solo los números mayores a 50, uno por línea.