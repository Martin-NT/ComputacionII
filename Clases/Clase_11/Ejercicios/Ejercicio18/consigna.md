## Ejercicio 18: Observación de Pipes con `lsof`

Ejecute un programa Python que use `os.pipe()` para comunicación entre procesos. Desde Bash, use `lsof -p [pid]` para observar los descriptores de archivo abiertos por el proceso.

---

## 🧪 ¿Cómo probarlo?
1. Ejecute desde la terminal:
```bash
python3 pipe_lsof.py
```

2. En otra terminal, mientras el script aún está corriendo, ejecutá:
- 👉 Para obtener el PID del padre:
```bash
ps aux | grep pipe_lsof.py
```
- Observar descriptores con lsof
```bash
lsof -p [PID_DEL_PADRE]
```

✅ Resultado esperado
- Verás que el proceso tiene un descriptor abierto de tipo PIPE.
- Comprobarás visualmente cómo el pipe está asociado al proceso en ejecución.

## Ejemplo
- En la carpeta pruebas pueden ver una captura de la prueba hecha, donde se ve en una linea:
El resultado de lsof -p 30816 te muestra todos los descriptores abiertos por el proceso pipe_lsof.py, y acá podés ver claramente que se está usando un pipe anónimo:
```bash
python3 30816 martin    4w  FIFO   0,14      0t0  200433 pipe
```

### ¿Qué significa cada campo de esta línea?
| Campo    | Valor  | Significado                                                 |
| -------- | ------ | ----------------------------------------------------------- |
| **FD**   | `4w`   | Descriptor de archivo 4, modo escritura (`w` = write)       |
| **TYPE** | `FIFO` | Es un pipe anónimo (First In First Out)                     |
| **NAME** | `pipe` | El nombre lógico: un pipe interno del kernel, no tiene ruta |

### Resumen:
- El proceso PID 30816 está escribiendo en un pipe anónimo (no tiene nombre en el sistema de archivos).
- El descriptor 4w indica que el proceso abrió ese pipe en modo escritura.
- Este tipo de pipe es común en la comunicación entre procesos padre-hijo con os.pipe().

Si el hijo estuviera vivo y leyendo, aparecería también un descriptor r (read) en el hijo apuntando al mismo NODE (200433 en tu caso).