## Ejercicio 7: Procesos Concurrentes con `multiprocessing`

Utilice `multiprocessing.Process` para crear 4 procesos que escriban su identificador y una marca de tiempo en un mismo archivo de log. Utilice `multiprocessing.Lock` para evitar colisiones.

---

## 🧠 Objetivo
- Crear 4 procesos que:
- Escriben su PID (identificador de proceso) y la fecha/hora actual.
- Guardan esa info en el mismo archivo de log.
- Usan un candado (Lock) para que escriban de a uno por vez.

## 🧪 ¿Cómo probarlo?

1. Ejecuta en tu terminal:
```bash
python3 ejercicio7.py
```

2. Se generará (o actualizará) el archivo log.txt en la misma carpeta. Al abrirlo, deberías ver algo como:
```bash
Proceso PID 34895 escribió en 2025-06-11 12:34:56
Proceso PID 34896 escribió en 2025-06-11 12:34:56
Proceso PID 34897 escribió en 2025-06-11 12:34:56
Proceso PID 34898 escribió en 2025-06-11 12:34:56

```
✅ Cada línea fue escrita sin interferencia, gracias al uso del Lock.

## 🛠️ ¿Qué pasaría sin el lock?
Si eliminás with lock: del código:
- Los procesos pueden escribir al mismo tiempo.
- Eso puede causar:
    - Texto mezclado en una línea.
    - Escrituras truncadas o solapadas.
    - Resultados impredecibles.
- Por eso el uso del Lock es esencial en escritura compartida.