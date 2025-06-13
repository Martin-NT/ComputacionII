#!/usr/bin/env python3
import argparse
import random

def main():
    parser = argparse.ArgumentParser(description="Genera números aleatorios")
    parser.add_argument('--n', type=int, required=True, help="Cantidad de números a generar")
    args = parser.parse_args()

    for _ in range(args.n):
        print(random.randint(0, 100))  # Imprime por stdout

if __name__ == "__main__":
    main()
