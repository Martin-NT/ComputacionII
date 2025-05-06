### Ejercicio 2 — FIFO como buffer entre procesos
**Objetivo**: Simular un flujo de datos continuo entre dos procesos.

**Instrucciones**:
1. Crear un proceso productor que escriba números del 1 al 100 en el FIFO con un `sleep(0.1)`.
2. Crear un consumidor que lea esos números del FIFO y los imprima con su timestamp local.
3. Asegurarse de que ambos scripts se ejecuten en paralelo.

**Extensión**: Agregar lógica en el consumidor para detectar si falta un número (por ejemplo, si no es consecutivo).

---

### Ejecución:
- Ejecutar el productor: python3 productor.py
- Ejecutar el consumidor: python3 consumidor.py