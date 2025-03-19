import argparse

def main():
    parser = argparse.ArgumentParser(description="Procesa archivos de entrada y salida")
    
    parser.add_argument("-f", "--file", help="Archivo de entrada", required=True)
    parser.add_argument("-o", "--output", help="Archivo de salida", required=True)

    args = parser.parse_args()
    
    print("Archivo de entrada:", args.file)
    print("Archivo de salida:", args.output)

if __name__ == "__main__":
    main()

"""Ejecutar en la terminal:"""
#   python3 script_argparse.py -f entrada.txt -o salida.txt

"""Salida esperada:"""
#   Archivo de entrada: entrada.txt
#   Archivo de salida: salida.txt

"""📌 Prueba también estos casos:"""
#1-Sin argumentos:
#   python3 script_argparse.py
#🔴 Esperado: Debe mostrar un error indicando que faltan -f y -o.

#2-Usa --help:
#   python3 script_argparse.py --help
#✅ Esperado: Debe mostrar la ayuda automática generada.

