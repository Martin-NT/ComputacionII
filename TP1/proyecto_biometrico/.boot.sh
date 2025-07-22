#!/bin/bash

# Verificar que el entorno virtual exista
if [ ! -d "venv" ]; then
  echo "El entorno virtual no existe. Ejecutá primero ./install.sh"
  exit 1
fi

# Activar entorno virtual
source venv/bin/activate

# Ejecutar el programa principal
python3 main.py

