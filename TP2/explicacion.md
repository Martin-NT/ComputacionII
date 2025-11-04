# Falta
- Tests
- Documentacion 
- Revisar que cumpla todo
- Que se ejecute sin fallas
- gitignore 

# Comandos que funcionan 
1. python3 server_processing.py -i 127.0.0.1 -p 9090
2. python3 server_scraping.py -i 0.0.0.0 -p 8000 --proc-ip 127.0.0.1 --proc-port 9090

- python3 client2.py 
- python3 client.py

- curl -s "http://127.0.0.1:8000/scrape?url=https://www.google.com" | python3 -m json.tool
- curl -s "http://127.0.0.1:8000/scrape?url=https://www.google.com" | python3 -c "import sys, json, base64; data=json.load(sys.stdin); img_data=base64.b64decode(data['processing_data']['screenshot']); sys.stdout.buffer.write(img_data)" > google_screenshot.png 

###  TERMINAL 1: Iniciar Servidor B (Procesamiento)
Este servidor escucha en un socket TCP y espera tareas.

```bash
python3 server_processing.py -i 127.0.0.1 -p 9090
python3 server_processing.py -i 127.0.0.1 -p 9000 -n 2

```
###  TERMINAL 2: Iniciar Servidor A

```bash
python3 server_scraping.py -i 0.0.0.0 -p 8000 --proc-ip 127.0.0.1 --proc-port 9090
python3 server_scraping.py -i 0.0.0.0 -p 8000

```

###  TERMINAL 3: 
```bash
curl -s "http://127.0.0.1:8000/scrape?url=https://example.com" | python3 -m json.tool
```

```bash
curl "http://127.0.0.1:8000/scrape?url=https://example.com"
```

python3 client.py https://example.com



curl -s "http://127.0.0.1:8000/scrape?url=https://example.com" | jq -r .processing_data.screenshot | base64 -d > screenshot.png

# Segun Gemini
python3 server_processing.py -i 127.0.0.1 -p 9090

python3 server_scraping.py -i 0.0.0.0 -p 8000 --proc-ip 127.0.0.1 --proc-port 9090

curl -s "http://127.0.0.1:8000/scrape?url=https://example.com" | python3 -m json.tool

curl -s "http://127.0.0.1:8000/scrape?url=https://example.com" | python3 -c "import sys, json, base64; data=json.load(sys.stdin); img_data=base64.b64decode(data['processing_data']['screenshot']); sys.stdout.buffer.write(img_data)" > screenshot.png














## 3. Ejemplo de Uso y Pruebas

Con los servidores A y B corriendo en sus terminales, puedes usar una tercera terminal para realizar las pruebas.

### Prueba 1: Probar Sistema Completo (Recomendado)

El script `client2.py` (o como lo hayas llamado) prueba toda la arquitectura:
1.  Se conecta al **Servidor A** (puerto 8000).
2.  Le pide analizar `https://example.com`.
3.  Imprime el JSON completo que recibe.
4.  Decodifica y guarda la imagen `screenshot_cliente.png`.

**Comando:**
```bash
python3 client2.py
```

**Salida Esperada:**
```
--- Prueba Completa: Analizando [https://example.com](https://example.com) ---

--- JSON Recibido del Servidor A: ---
{
    "url": "[https://example.com](https://example.com)",
    "timestamp": "...",
    "scraping_data": { ... },
    "processing_data": {
        "screenshot": "iVBORw0KGgo...",
        ...
    },
    "status": "success"
}
--------------------------------------

Procesando y guardando screenshot...
✅ ¡Imagen guardada como screenshot_cliente.png!
```

---

### Prueba 2: Probar con `curl` (Para URLs personalizadas)

Si quieres probar rápidamente con **otras URLs** sin modificar el script, puedes usar `curl`.

**Para ver solo el JSON formateado:**
(Cambia `https://google.com` por la URL que quieras)
```bash
curl -s "[http://127.0.0.1:8000/scrape?url=https://google.com](http://127.0.0.1:8000/scrape?url=https://google.com)" | python3 -m json.tool
```

**Para guardar solo la imagen (sin ver el JSON):**
(Cambia `https...` y `google.png` por lo que quieras)
```bash
curl -s "[http://127.0.0.1:8000/scrape?url=https://google.com](http://127.0.0.1:8000/scrape?url=https://google.com)" | python3 -c "import sys, json, base64; data=json.load(sys.stdin); img_data=base64.b64decode(data['processing_data']['screenshot']); sys.stdout.buffer.write(img_data)" > google.png
```

---

### Prueba 3: Probar SÓLO el Servidor B

El script `client.py` original prueba la conexión directa por socket al **Servidor B** (puerto 9090).

**Comando:**
```bash
python3 client.py
```

**Salida Esperada:**
```
ok ['screenshot', 'performance', 'thumbnails']
```












# TP2 - Sistema de Scraping y Análisis Web Distribuido

Este proyecto implementa un sistema distribuido de scraping y análisis web en Python, basado en la consigna del TP2 de Computación II. El sistema se compone de dos servidores que trabajan de forma coordinada.

* **Servidor A (`server_scraping.py`):** Un servidor HTTP asíncrono (AsyncIO) que actúa como *frontend*. Recibe peticiones de los clientes, realiza el scraping básico y delega el procesamiento pesado.
* **Servidor B (`server_processing.py`):** Un servidor TCP de procesamiento (Multiprocessing) que actúa como *backend*. Recibe tareas del Servidor A y ejecuta operaciones CPU-bound (como tomar screenshots o analizar imágenes) en un pool de procesos.

---

## 1. Instalación

Se requiere Python 3.8 o superior.

### a. Entorno Virtual y Dependencias

Se recomienda crear un entorno virtual para instalar las dependencias.

```bash
# Crear el entorno
python3 -m venv env

# Activar el entorno (Linux/macOS)
source env/bin/activate
# (En Windows usar: env\Scripts\activate)
```

Crea un archivo `requirements.txt` con el siguiente contenido:

**`requirements.txt`**
```
aiohttp
beautifulsoup4
lxml
Pillow
requests
playwright
```

Luego, instala todas las dependencias:
```bash
pip install -r requirements.txt
```

### b. Instalación de Navegadores (Playwright)

El Servidor B (`processor/screenshot.py`) usa Playwright para tomar capturas de pantalla. Debes instalar el navegador (Chromium) que utiliza:

```bash
playwright install chromium
```

---

## 2. Ejecución del Sistema

Para que el sistema funcione, debes tener **ambos servidores corriendo** al mismo tiempo en dos terminales separadas. Asegúrate de tener el entorno virtual activado en ambas.

### 💻 Terminal 1: Iniciar Servidor B (Procesamiento)

Este servidor escucha en un socket TCP y espera tareas.

```bash
# Escucha en 127.0.0.1, puerto 9090, con un pool de procesos
python3 server_processing.py -i 127.0.0.1 -p 9090
```
*Deberías ver:* `[B] listening on 127.0.0.1:9090 (pool=...)`

### 💻 Terminal 2: Iniciar Servidor A (Scraping)

Este servidor escucha peticiones HTTP y se conecta al Servidor B.

```bash
# Escucha HTTP en 0.0.0.0, puerto 8000
# Se conecta al Servidor B en 127.0.0.1:9090
python3 server_scraping.py -i 0.0.0.0 -p 8000 --proc-ip 127.0.0.1 --proc-port 9090
```
*Deberías ver:* `======== Running on http://0.0.0.0:8000 ========`

---

## 3. Ejemplo de Uso y Pruebas

Con los dos servidores corriendo, abre una **tercera terminal** (con el entorno activado) para ejecutar las pruebas de cliente.

### Prueba 1: Probar Sistema Completo (Recomendado)

El script `client2.py` (el cliente HTTP mejorado) prueba toda la arquitectura:
1.  Se conecta al **Servidor A** (puerto 8000).
2.  Le pide analizar `https://example.com`.
3.  Imprime el JSON completo que recibe.
4.  Decodifica y guarda la imagen `screenshot_cliente.png`.

**Comando:**
```bash
python3 client2.py
```

**Salida Esperada:**
```
--- Prueba Completa: Analizando [https://example.com](https://example.com) ---

--- JSON Recibido del Servidor A: ---
{
    "url": "[https://example.com](https://example.com)",
    "timestamp": "...",
    "scraping_data": { ... },
    "processing_data": {
        "screenshot": "iVBORw0KGgo...",
        ...
    },
    "status": "success"
}
--------------------------------------

Procesando y guardando screenshot...
✅ ¡Imagen guardada como screenshot_cliente.png!
```

---

### Prueba 2: Probar con `curl` (Para URLs personalizadas)

Si quieres probar rápidamente con **otras URLs** sin modificar el script, puedes usar `curl`.

**Para ver solo el JSON formateado:**
(Cambia `https://google.com` por la URL que quieras)
```bash
curl -s "[http://127.0.0.1:8000/scrape?url=https://google.com](http://127.0.0.1:8000/scrape?url=https://google.com)" | python3 -m json.tool
```

**Para guardar solo la imagen (sin ver el JSON):**
(Cambia `https...` y `google.png` por lo que quieras)
```bash
curl -s "[http://127.0.0.1:8000/scrape?url=https://google.com](http://127.0.0.1:8000/scrape?url=https://google.com)" | python3 -c "import sys, json, base64; data=json.load(sys.stdin); img_data=base64.b64decode(data['processing_data']['screenshot']); sys.stdout.buffer.write(img_data)" > google.png && echo "✅ Imagen guardada como google.png"
```

---

### Prueba 3: Probar SÓLO el Servidor B

El script `client.py` original prueba la conexión directa por socket al **Servidor B** (puerto 9090).

**Comando:**
```bash
python3 client.py
```

**Salida Esperada:**
```
ok ['screenshot', 'performance', 'thumbnails']
```