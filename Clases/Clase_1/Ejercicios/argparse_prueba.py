import argparse

def main():
    parser = argparse.ArgumentParser(description="Procesa archivos de entrada y salida")
    
    parser.add_argument("-f", "--file", help="Archivo de entrada", required=True)
    parser.add_argument("-o", "--output", help="Archivo de salida", required=True)
    parser.add_argument("-v", "--verbose", help="Muestra mensajes adicionales", action="store_true")
     
    args = parser.parse_args()
    
    print("Archivo de entrada:", args.file)
    print("Archivo de salida:", args.output)

    if args.verbose:
        print("Procesamiento en curso...")

if __name__ == "__main__":
    main()


#python3 script.py -f entrada.txt -o salida.txt -v


"""📌 Desafío práctico
Ahora te toca a ti. Quiero que crees un script con argparse que:

Reciba un archivo de entrada y un archivo de salida.
Tenga un argumento opcional --verbose que, si se activa, muestre un mensaje extra como "Procesamiento en curso...".
Muestre un error si no se proporcionan los archivos obligatorios.
📌 Sugerencias:

Usa required=True para los argumentos obligatorios.
Usa action="store_true" para --verbose.
Prueba escribir el código y dime si necesitas ayuda. ¡Tú puedes! 🚀"""