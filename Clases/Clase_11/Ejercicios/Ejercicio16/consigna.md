## Ejercicio 16: Recolección Manual de Estado de Hijos

Implemente en Python un programa que cree 3 hijos que finalizan en distinto orden. El padre deberá recolectar manualmente cada estado usando `os.waitpid`, y registrar en qué orden terminaron.

---
## 🧪 ¿Cómo probarlo?
1. Ejecuta desde la terminal:
```bash
python3 ejercicio16.py
```

## 📌 ¿Qué hace?
- El proceso padre crea 3 hijos con os.fork().
- Cada hijo duerme un tiempo aleatorio entre 1 y 5 segundos.
- El padre recolecta manualmente a los hijos en el orden que finalizan usando os.waitpid(-1, 0).
- Guarda y muestra el orden de finalización.