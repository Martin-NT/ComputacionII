# Resumen: Manejo de Argumentos en la Línea de Comandos con Python

## 1. Conceptos Clave
- `getopt`: Manejo básico de argumentos de línea de comandos, útil para opciones simples.
- `argparse`: Herramienta más flexible y moderna para definir argumentos en scripts de Python.
- **Diferencias clave:**
  - `getopt` es más manual y limitado.
  - `argparse` genera ayuda automática y permite validaciones avanzadas.

## 2. Uso de `getopt`
```python
import sys
import getopt

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:o:", ["file=", "output="])
    except getopt.GetoptError as err:
        print("Error:", err)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-f", "--file"):
            file_name = arg
        elif opt in ("-o", "--output"):
            output_name = arg

    print("Archivo de entrada:", file_name)
    print("Archivo de salida:", output_name)

if __name__ == "__main__":
    main()
```
### **Ejemplo de ejecución:**
```bash
python script_getopt.py -f entrada.txt -o salida.txt
```

## 3. Uso de `argparse`
```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="Procesa archivos de entrada y salida")
    parser.add_argument("-f", "--file", help="Archivo de entrada", required=True)
    parser.add_argument("-o", "--output", help="Archivo de salida", required=True)
    parser.add_argument("-v", "--verbose", help="Modo detallado", action="store_true")
    args = parser.parse_args()
    
    print("Archivo de entrada:", args.file)
    print("Archivo de salida:", args.output)
    if args.verbose:
        print("Procesamiento en curso...")

if __name__ == "__main__":
    main()
```
### **Ejemplo de ejecución:**
```bash
python script_argparse.py -f entrada.txt -o salida.txt -v
```

## 4. Ventajas de `argparse` sobre `getopt`
✅ Genera ayuda automática con `--help`.
✅ Permite definir argumentos obligatorios y opcionales.
✅ Soporta validación de tipos de datos.
✅ Permite múltiples valores en un solo argumento.

## 5. Preguntas de Repaso con Respuestas
1. **¿Cuál es la ventaja principal de `argparse` sobre `getopt`?**  
   `argparse` es más flexible y permite una mejor estructura de argumentos, incluyendo validaciones, tipos de datos y generación automática de mensajes de ayuda.

2. **¿Cómo defines un argumento obligatorio en `argparse`?**  
   Se usa `required=True`, por ejemplo:
   ```python
   parser.add_argument("-f", "--file", help="Archivo de entrada", required=True)
   ```

3. **¿Qué comando usas para ver la ayuda de un script con `argparse`?**  
   Ejecutando el script con `--help`, por ejemplo:
   ```bash
   python script_argparse.py --help
   ```

## 6. Recursos Adicionales
- 📖 [Documentación oficial de `argparse`](https://docs.python.org/3/library/argparse.html)
- 📖 [Tutorial de `argparse` en Real Python](https://realpython.com/command-line-interfaces-python-argparse/)

---

