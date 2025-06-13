#!/usr/bin/env python3
# “Usá el intérprete python3 para ejecutar este archivo.”
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Filtra números mayores que un mínimo")
    parser.add_argument('--min', type=int, required=True, help="Valor mínimo")
    args = parser.parse_args()

    for linea in sys.stdin:
        try:
            num = int(linea.strip())
            if num > args.min:
                print(num)
        except ValueError:
            continue  # ignora líneas no numéricas

if __name__ == "__main__":
    main()
