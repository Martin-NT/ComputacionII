#!/bin/bash

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

echo "¡Entorno virtual creado y dependencias instaladas!"
echo "Para activar el entorno, ejecutá: source venv/bin/activate"

