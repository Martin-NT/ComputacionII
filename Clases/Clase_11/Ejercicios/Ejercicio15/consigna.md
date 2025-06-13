## Ejercicio 15: Análisis de Procesos Activos

Desde Bash, cree un script que recorra `/proc` y liste los procesos activos, mostrando para cada uno su PID, PPID, nombre del ejecutable y estado (`cat /proc/[pid]/status`). Genere un resumen con los distintos estados encontrados.

---

## 🧪 ¿Cómo probarlo?
1. Dale de permisos de ejecución:
```bash
chmod +x analizar_procesos.sh
```

2. Ejecutalo:
```bash
./analizar_procesos.sh
```

## 📌 ¿Qué muestra?
Una tabla con:
    - PID: ID del proceso
    - PPID: ID del padre
    - Nombre: nombre del ejecutable
    - Estado: primera letra del estado (ej: R, S, Z, etc.)

Al final, un resumen con cuántos procesos hay en cada estado:
| Estado | Significado |
| ------ | ----------- |
| R      | Running     |
| S      | Sleeping    |
| D      | I/O wait    |
| Z      | Zombie      |
| T      | Stopped     |

El script recorre todos los procesos en ejecución dentro del sistema leyendo directamente el archivo /proc/[pid]/status para obtener el PID, PPID, nombre del proceso y su estado. Se identificaron 3 tipos de estados:
    - S (Sleeping): 226 procesos
    - R (Running): 4 procesos
    - I (Idle): 77 procesos

Esto indica que la mayoría de los procesos están dormidos esperando eventos, unos pocos están activos, y varios son procesos del kernel en estado inactivo.