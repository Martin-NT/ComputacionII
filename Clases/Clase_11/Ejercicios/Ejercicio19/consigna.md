## Ejercicio 19: Monitoreo de Escritura Concurrente sin Exclusión

Ejecute desde Bash varios procesos Python que escriban a un mismo archivo sin usar `Lock`. Observe y compare el resultado con la versión sincronizada usando `multiprocessing.Lock`.

---
## 🧪 ¿Cómo probarlo?
### Parte 1: Sin exclusión mutua (sin Lock)
1. Ejecute desde la terminal:
```bash
python3 escritor_sin_lock.py
cat salida.txt
```
#### 🔍 Qué observar:
- Las líneas del archivo pueden estar mezcladas o solapadas.
- No se garantiza el orden ni la integridad de los datos.

### Parte 2: Con exclusión mutua (con Lock)
1. Borra el archivo anterior:
```bash
rm salida.txt
```
2. Ejecutá el script:
```bash
python3 escritor_con_lock.py
cat salida.txt
```
#### ✅ Qué cambia:
- Las líneas de cada proceso aparecen juntas y completas.
- No hay corrupción ni entremezcla, porque el acceso al archivo está protegido con Lock.