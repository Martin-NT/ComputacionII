import sys
import getopt

def main():
    file_name = ""
    output_name = ""

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

""" Explicación del código:"""
#   sys.argv[1:] obtiene los argumentos pasados desde la terminal.
#   getopt.getopt() define las opciones cortas (-f, -o) y largas (--file, --output).
#   Un bucle for recorre las opciones y almacena los valores en variables.
#   Si el usuario no introduce argumentos correctos, se muestra un error.

"""Para ejecutar en la terminal:"""
#   python3 script_getopt.py -f entrada.txt -o salida.txt

"""Salida esperada"""
#   Archivo de entrada: entrada.txtArchivo de entrada: entrada.txt
#   Archivo de salida: salida.txt
