
# TP2 - Sistema de Scraping y Análisis Web Distribuido

## Información   
- **Nombre:** Martin Navarro
- **Legajo:** 62181
- **Correo:** mt.navarro@alumno.um.edu.ar
- **Materia**: Computación II

## Descripción

Trabajo práctico de la materia Computación II. El objetivo es implementar un sistema distribuido de scraping y análisis web. El sistema utiliza un servidor HTTP asíncrono (Servidor A) como frontend y un servidor TCP con procesamiento paralelo (Servidor B) como backend.

---

## 📁 Estructura del Proyecto

| Archivo | Descripción |
|--------|-------------|
| `server_scraping.py` | Servidor A: Servidor HTTP (asyncio) que recibe peticiones del cliente. |
| `server_processing.py` | Servidor B: Servidor TCP (multiprocessing) que realiza el trabajo pesado.. |
| `common/protocol.py` | Protocolo de sockets para client.py. |
| `common/serialization.py` | Funciones auxiliares para serialización JSON. |
| `scraper/async_http.py` | Cliente HTTP asíncrono (aiohttp) para descargar HTML. |
| `scraper/html_parser.py` | Extrae título, links, headers e imágenes del HTML. |
| `scraper/metadata_extractor.py` | Extrae las meta tags (description, keywords, etc.). |
| `processor/screenshot.py` | Genera el screenshot de la página web (Playwright) |
| `processor/performance.py` | Calcula el rendimiento de la página (requests). |
| `processor/image_processor.py` | Descarga imágenes y genera thumbnails (Pillow). |
| `client.py` | Cliente de prueba simple para conectar directo al Servidor B (Socket). |
| `client2.py` | Cliente de prueba completo para conectar al Servidor A (HTTP). |
| `tests/test_processor.py` | Test de integración para el Servidor B. |
| `tests/test_scraper.py` | Test de integración para el Servidor A. |
| `requirements.txt` | Lista de dependencias de Python necesarias (ej: aiohttp, playwright). |
| `.gitignore` | Archivos y carpetas excluidos del repositorio (ej: `env/`, `__pycache__/`). |
| `README.md` | Este archivo con toda la información del proyecto. |

---

## 📦 Requisitos

- Python 3.8 o superior
- (Recomendado) Uso de entorno virtual (venv)
- Instalar dependencias definidas en requirements.txt (Paso 5 de Instalación)

---

## 1. Instalación

1. Clonar el repositorio
```bash
git clone git@github.com:Martin-NT/ComputacionII.git
```

2. Ubicarse en el proyecto
```bash
cd ComputacionII/TP2
```

3. Crear entorno virtual
```bash
python3 -m venv env
```

4. Activar entorno virtual
```bash
source env/bin/activate
```

5. Instalar dependencias
```bash
pip install -r requirements.txt
```
6. Instalar Navegadores (Playwright)
```bash
playwright install chromium
```

## 2. Ejecucion del Sistema
Para que el sistema funcione, debes tener **ambos servidores corriendo** al mismo tiempo en dos terminales separadas. Asegúrate de tener el entorno virtual (`venv`) activado en ambas.

### Terminal 1: Iniciar Servidor B
```bash
python3 server_processing.py -i 127.0.0.1 -p 9090 -n 2
```
- **Nota:** Si omites el `-n 2`, el servidor usará por defecto todos los núcleos de tu CPU (`mp.cpu_count()`), no del navegador.

### 💻 Terminal 2: Iniciar Servidor A (Scraping)

Este es el servidor principal que atiende a los clientes. Escucha en el puerto `8000` y se conecta al Servidor B en el puerto `9090`.
```bash
python3 server_scraping.py -i 0.0.0.0 -p 8000 --proc-ip 127.0.0.1 --proc-port 9090
```

## 3. Comandos de Prueba

Con los dos servidores corriendo, abre una **tercera terminal** (con el entorno activado) para ejecutar las pruebas.

### Prueba A: Cliente Python Completo (Recomendado)

El script `client2.py` (el cliente HTTP mejorado) prueba toda la arquitectura:
1.  Se conecta al **Servidor A** (puerto 8000).
2.  Imprime el JSON completo que recibe de `https://example.com`.
3.  Decodifica y guarda la imagen `screenshot_cliente.png`.

**Comando:**
```bash
python3 client2.py
```

### Prueba B: Probar SÓLO el Servidor B

El script `client.py` original prueba la conexión directa por socket al **Servidor B** (puerto 9090).

**Comando:**
```bash
python3 client.py
```
- **Salida Esperada:** `ok ['screenshot', 'performance', 'thumbnails']`

### Prueba C: Probar con `curl` 

#### Para ver JSON de otra URL
Si quieres probar rápidamente con **otra URL** y solo ver el JSON en la terminal.

```bash
curl -s "http://127.0.0.1:8000/scrape?url=https://www.google.com" | python3 -m json.tool
```

#### Para guardar imagen de otra URL
Si quieres probar con **otra URL** y guardar su screenshot directamente.

```bash
curl -s "http://127.0.0.1:8000/scrape?url=https://www.google.com" | python3 -c "import sys, json, base64; data=json.load(sys.stdin); img_data=base64.b64decode(data['processing_data']['screenshot']); sys.stdout.buffer.write(img_data)" > google_screenshot.png 
```

## 4. Correr los Tests
Para que el sistema funcione, debes tener **ambos servidores corriendo** al mismo tiempo en dos terminales separadas. Asegúrate de tener el entorno virtual (`venv`) activado en ambas.

# Prueba del Servidor B
- **Requiere:** Que el **Servidor B** (`server_processing.py`) esté corriendo en la Terminal 1 y el entorno virtual activado en la nueva terminal.
- **Comando:**
    ```bash
    python3 tests/test_processor.py
    ```
- **Salida esperada:** `✅ PRUEBA SERVIDOR B: EXITOSA.`

# Prueba del Servidor A (y la integración con B)
- **Requiere:** Que **AMBOS servidores** (A y B) estén corriendo en sus terminales y el entorno virtual activado en la nueva terminal.
- **Comando:**
    ```bash
    python3 tests/test_scraper.py
    ```
- **Salida esperada:** `✅ PRUEBA SERVIDOR A (INTEGRACIÓN): EXITOSA.`

---
