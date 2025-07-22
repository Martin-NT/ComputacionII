#!/bin/bash

# Crear entorno si no existe
if [ ! -d "env" ]; then
    python3 -m venv env
fi

# Activar entorno
source env/bin/activate

# Instalar requisitos
pip install -r requirements.txt

