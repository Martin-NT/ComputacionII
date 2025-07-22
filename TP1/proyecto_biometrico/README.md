# Sistema Concurrente de Análisis Biométrico con Cadena de Bloques Local

## Autor: Martin Navarro Teixidor

## Descripción

Trabajo práctico de la materia Computación 2. El objetivo es construir un sistema concurrente y distribuido en procesos, que genere, procese y almacene datos biométricos en una cadena de bloques local.

---

## Estructura del Proyecto

- `main.py`: Script principal que genera los datos biométricos.
- `blockchain.json`: Archivo que almacena la cadena de bloques.
- `verificar_cadena.py`: Script para verificar la integridad de la blockchain.
- `reporte.txt`: Reporte con estadísticas finales.

---

## Requisitos

- Python 3.9 o superior
- (Recomendado) entorno virtual
- Dependencias en `requirements.txt`
- Uso de módulos estándar: `multiprocessing`, `queue`, `json`, `datetime`, `random`, `hashlib`
- Comunicación entre procesos con `Pipe` y `Queue`
- Sincronización con primitivas `Lock`, `Semaphore` y `Event`
- El programa finaliza limpiamente sin procesos zombies ni recursos abiertos

---

## Instalación

- **Paso 1**
git clone git@github.com:Martin-NT/ComputacionII.git
- **Paso 2**
cd proyecto_biometrico
- **Paso 3**
chmod +x install.sh
- **Paso 4**
chmod +x boot.sh
- **Paso 5**
./install.sh
- **Paso 6**
./boot.sh
- **Paso 7**
python3 verificar_cadena.py