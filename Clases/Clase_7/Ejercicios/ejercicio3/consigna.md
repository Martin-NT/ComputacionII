# Ejercicio 3: Ignorar señales temporalmente

**Objetivo:** Controlar cuándo un programa debe responder a una señal.

**Enunciado:**
Crea un programa que ignore `SIGINT` (Ctrl+C) durante los primeros 5 segundos de ejecución. Luego, el programa debe restaurar el comportamiento por defecto para esa señal y continuar ejecutando indefinidamente. Verifica que `Ctrl+C` no interrumpe el programa durante los primeros segundos, pero sí lo hace después.

---

## Probarlo

1. Ejecuta el programa.
2. Prueba presionar Ctrl+C durante los primeros 5 segundos. No debería interrumpir el programa.
3. Luego de 5 segundos, presiona Ctrl+C nuevamente y el programa debería interrumpirse.