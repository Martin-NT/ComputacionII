# COMPUTACIÓN II

## TP2 - Sistema de Scraping y Análisis Web Distribuido

**Fecha de entrega: 14/11/2025**

### Información   
- **Nombre:** Martin Navarro
- **Legajo:** 62181
- **Correo:** mt.navarro@alumno.um.edu.ar
- **Materia**: Computación II

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

## 📦 Requisitos

- Python 3.8 o superior
- (Recomendado) Uso de entorno virtual (venv)
- Instalar dependencias definidas en requirements.txt (Paso 5 de Instalación)

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
- **Salida esperada:** `[B] listening on 127.0.0.1:9090 (pool=2)`

### 💻 Terminal 2: Iniciar Servidor A (Scraping)

Este es el servidor principal que atiende a los clientes. Escucha en el puerto `8000` y se conecta al Servidor B en el puerto `9090`.
```bash
python3 server_scraping.py -i 0.0.0.0 -p 8000 --proc-ip 127.0.0.1 --proc-port 9090
```
- **Salida esperada:** `======== Running on http://0.0.0.0:8000 ========`

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

## **Problema**

Se requiere desarrollar un sistema distribuido de scraping y análisis web utilizando Python. El sistema debe consistir en dos servidores que trabajan de forma coordinada para extraer, analizar y procesar información de sitios web.

---

### **Parte A: Servidor de Extracción Asíncrono**

Implementar un servidor HTTP utilizando **asyncio** que maneje las solicitudes de scraping de forma asíncrona. Este servidor debe:

- Recibir URLs de sitios web a analizar a través de peticiones HTTP
- Realizar el scraping de la página web de forma asíncrona sin bloquear el event loop
- Extraer la siguiente información de cada URL:
  - Título de la página
  - Todos los enlaces (links) encontrados
  - Meta tags relevantes (description, keywords, Open Graph tags)
  - Cantidad de imágenes en la página
  - Estructura básica (cantidad de headers H1-H6)
- Comunicarse con el servidor de procesamiento (Parte B) para solicitar análisis adicional
- Esperar de forma asíncrona los resultados del servidor de procesamiento
- Devolver al cliente una respuesta JSON consolidada con toda la información extraída y procesada

El servidor debe implementar mecanismos de comunicación asíncrona entre tareas para coordinar el scraping y el procesamiento sin bloquear operaciones.

---

### **Parte B: Servidor de Procesamiento con Multiprocessing**

Implementar un servidor utilizando **multiprocessing** y **socketserver** que procese tareas computacionalmente intensivas. Este servidor debe:

- Escuchar conexiones en un puerto diferente al servidor principal
- Recibir solicitudes del Servidor A a través de sockets
- Ejecutar las siguientes operaciones en procesos separados:
  - **Captura de screenshot**: Generar una imagen (PNG) de cómo se ve la página web renderizada
  - **Análisis de rendimiento**: Calcular el tiempo de carga, tamaño total de recursos, cantidad de requests necesarios
  - **Análisis de imágenes**: Descargar las imágenes principales de la página y generar thumbnails optimizados
- Manejar múltiples solicitudes concurrentemente utilizando un pool de procesos
- Devolver los resultados al Servidor A a través del socket

La comunicación entre ambos servidores debe realizarse mediante sockets y utilizar serialización apropiada (JSON, pickle, o protocol buffers).

---

### **Parte C: Transparencia para el Cliente**

El cliente debe interactuar únicamente con el Servidor A (asyncio). Todas las operaciones de procesamiento realizadas por el Servidor B deben ser completamente transparentes para el cliente. 

El servidor A debe:
- Recibir la petición del cliente
- Coordinar automáticamente con el Servidor B cuando sea necesario
- Consolidar todos los resultados
- Devolver una respuesta única al cliente

Desde la perspectiva del cliente, todo el procesamiento debe parecer que ocurre en un solo servidor.

---

## **Requerimientos Técnicos**

### **Funcionalidad Mínima**

- La aplicación debe contener como mínimo **4 funciones principales**:
  1. Scraping de contenido HTML
  2. Extracción de metadatos
  3. Generación de screenshot
  4. Análisis de rendimiento

### **Networking**

- El Servidor A debe soportar conexiones **IPv4 e IPv6** indistintamente
- Implementar manejo de errores de red (timeouts, conexiones rechazadas, etc.)
- El Servidor B debe escuchar en un puerto diferente y manejar protocolo de comunicación binario eficiente

### **Concurrencia y Paralelismo**

- Uso obligatorio de **asyncio** para el Servidor A:
  - Manejo asíncrono de múltiples clientes
  - Requests HTTP asíncronos (usar `aiohttp`)
  - Comunicación asíncrona entre componentes
  
- Uso obligatorio de **multiprocessing** para el Servidor B:
  - Pool de workers para procesamiento paralelo
  - Manejo de tareas CPU-bound en procesos separados
  - Sincronización apropiada entre procesos

### **Interfaz de Línea de Comandos**

Implementar parsing de argumentos con **argparse** (o **getopt**):

```bash
# Servidor Principal (Parte A)
$ ./server_scraping.py -h
usage: server_scraping.py [-h] -i IP -p PORT [-w WORKERS]

Servidor de Scraping Web Asíncrono

Opciones:
  -h, --help            Muestra este mensaje de ayuda
  -i IP, --ip IP        Dirección de escucha (soporta IPv4/IPv6)
  -p PORT, --port PORT  Puerto de escucha
  -w WORKERS, --workers WORKERS
                        Número de workers (default: 4)

# Servidor de Procesamiento (Parte B)
$ ./server_processing.py -h
usage: server_processing.py [-h] -i IP -p PORT [-n PROCESSES]

Servidor de Procesamiento Distribuido

Opciones:
  -h, --help            Muestra este mensaje de ayuda
  -i IP, --ip IP        Dirección de escucha
  -p PORT, --port PORT  Puerto de escucha
  -n PROCESSES, --processes PROCESSES
                        Número de procesos en el pool (default: CPU count)
```

### **Manejo de Errores**

Implementar manejo robusto de errores:
- URLs inválidas o inaccesibles
- Timeouts en scraping (máximo 30 segundos por página)
- Errores de comunicación entre servidores
- Recursos no disponibles (imágenes, CSS, etc.)
- Límites de memoria para páginas muy grandes

### **Formato de Respuesta**

El servidor debe devolver un JSON con la siguiente estructura:

```json
{
  "url": "https://ejemplo.com",
  "timestamp": "2024-11-10T15:30:00Z",
  "scraping_data": {
    "title": "Título de la página",
    "links": ["url1", "url2", "..."],
    "meta_tags": {
      "description": "...",
      "keywords": "...",
      "og:title": "..."
    },
    "structure": {
      "h1": 2,
      "h2": 5,
      "h3": 10
    },
    "images_count": 15
  },
  "processing_data": {
    "screenshot": "base64_encoded_image",
    "performance": {
      "load_time_ms": 1250,
      "total_size_kb": 2048,
      "num_requests": 45
    },
    "thumbnails": ["base64_thumb1", "base64_thumb2"]
  },
  "status": "success"
}
```

---

## **Bonus Track** (Puntos Extra)

### **Opción 1: Sistema de Cola con IDs de Tarea**

Implementar un sistema asíncrono de cola de trabajos:

- El servidor A devuelve inmediatamente un **task_id** al cliente
- El cliente puede consultar el estado de la tarea con ese ID:
  ```
  GET /status/{task_id}
  ```
- Estados posibles: `pending`, `scraping`, `processing`, `completed`, `failed`
- Cuando esté completa, el cliente puede descargar los resultados:
  ```
  GET /result/{task_id}
  ```

### **Opción 2: Rate Limiting y Caché**

- Implementar rate limiting por dominio (máximo N requests por minuto al mismo dominio)
- Sistema de caché: si una URL ya fue scrapeada recientemente (< 1 hora), devolver resultado cacheado
- Usar Redis o un diccionario compartido con TTL

### **Opción 3: Análisis Avanzado**

Agregar análisis adicional en el Servidor B:
- Detección de tecnologías usadas (frameworks JS, CMS, etc.)
- Análisis de SEO (score de optimización)
- Extracción de esquemas estructurados (JSON-LD, Schema.org)
- Análisis de accesibilidad (contraste de colores, alt tags)

---

## **Objetivos de Aprendizaje**

Al completar este trabajo práctico, el estudiante será capaz de:

1. **Programación Asíncrona**:
   - Diseñar y implementar servidores con asyncio
   - Manejar I/O no bloqueante eficientemente
   - Coordinar múltiples tareas asíncronas concurrentes

2. **Programación Paralela**:
   - Utilizar multiprocessing para tareas CPU-bound
   - Diseñar arquitecturas con pools de procesos
   - Implementar comunicación inter-proceso (IPC)

3. **Networking**:
   - Implementar protocolos de comunicación cliente-servidor
   - Manejar sockets TCP para comunicación entre servicios
   - Soportar IPv4 e IPv6

4. **Web Scraping**:
   - Extraer información de páginas web usando BeautifulSoup/lxml
   - Manejar diferentes estructuras HTML
   - Procesar y normalizar datos extraídos

5. **Arquitectura de Sistemas Distribuidos**:
   - Diseñar sistemas con múltiples componentes independientes
   - Implementar transparencia de distribución
   - Manejar fallos y errores en sistemas distribuidos

---

## **Dependencias Requeridas**

```bash
pip install aiohttp beautifulsoup4 lxml Pillow selenium aiofiles
```

Opcional para screenshots:
```bash
# ChromeDriver o GeckoDriver para Selenium
# O usar playwright: pip install playwright && playwright install
```

---

## **Estructura de Proyecto Sugerida**

```
TP2/
├── server_scraping.py          # Servidor asyncio (Parte A)
├── server_processing.py        # Servidor multiprocessing (Parte B)
├── client.py                   # Cliente de prueba
├── scraper/
│   ├── __init__.py
│   ├── html_parser.py          # Funciones de parsing HTML
│   ├── metadata_extractor.py  # Extracción de metadatos
│   └── async_http.py           # Cliente HTTP asíncrono
├── processor/
│   ├── __init__.py
│   ├── screenshot.py           # Generación de screenshots
│   ├── performance.py          # Análisis de rendimiento
│   └── image_processor.py      # Procesamiento de imágenes
├── common/
│   ├── __init__.py
│   ├── protocol.py             # Protocolo de comunicación
│   └── serialization.py        # Serialización de datos
├── tests/
│   ├── test_scraper.py
│   └── test_processor.py
├── requirements.txt
└── README.md
```

---

## **Criterios de Evaluación**

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| Funcionalidad completa | 30 | Todas las partes A, B y C funcionan correctamente |
| Uso correcto de asyncio | 20 | Servidor asíncrono eficiente, no hay bloqueos del event loop |
| Uso correcto de multiprocessing | 20 | Pool de procesos funcionando, IPC correcta |
| Manejo de errores | 10 | Errores manejados apropiadamente en todos los casos |
| Calidad de código | 10 | Código limpio, modular, bien documentado |
| Interfaz CLI | 5 | Argumentos parseados correctamente, ayuda clara |
| Bonus Track | +15 | Implementación de features opcionales |

**Total**: 95 puntos (+ 15 bonus)

---

## **Referencias**

- **AsyncIO Documentation**: [https://docs.python.org/3/library/asyncio.html](https://docs.python.org/3/library/asyncio.html)
- **aiohttp Documentation**: [https://docs.aiohttp.org/](https://docs.aiohttp.org/)
- **Multiprocessing Documentation**: [https://docs.python.org/3/library/multiprocessing.html](https://docs.python.org/3/library/multiprocessing.html)
- **SocketServer Documentation**: [https://docs.python.org/3/library/socketserver.html](https://docs.python.org/3/library/socketserver.html)
- **BeautifulSoup Documentation**: [https://www.crummy.com/software/BeautifulSoup/bs4/doc/](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- **Selenium Documentation**: [https://selenium-python.readthedocs.io/](https://selenium-python.readthedocs.io/)

---

## **Instrucciones de Entrega**

1. **Repositorio**: Subir el proyecto al repositorio personal de GitHub/GitLab
2. **Carpeta**: Debe estar en una carpeta llamada exactamente `TP2`
3. **README**: Incluir instrucciones de instalación y ejecución
4. **Fecha límite**: 14/11/2025 - 23:59 hs

---

## **Consejos y Recomendaciones**

### **Para el Servidor Asyncio**

- Usa `aiohttp.ClientSession` con timeout configurado
- No uses `requests` (es bloqueante), siempre `aiohttp`
- Implementa un límite de conexiones concurrentes por dominio
- Maneja excepciones específicas de asyncio (`asyncio.TimeoutError`, etc.)

### **Para el Servidor Multiprocessing**

- Usa `ProcessPoolExecutor` o `Pool` de multiprocessing
- Ten cuidado con objetos no serializables (no se pueden pasar entre procesos)
- Usa `Queue` o `Pipe` para comunicación inter-proceso si es necesario
- Cierra el pool apropiadamente con context managers

### **Para Screenshots**

- Considera usar modo headless para eficiencia
- Configura timeouts para páginas que tardan mucho
- Maneja páginas que requieren JavaScript vs HTML estático

### **Para la Comunicación entre Servidores**

- Define un protocolo claro (ej: longitud del mensaje + mensaje)
- Serializa con `json` o `pickle` según necesidad
- Implementa reintentos en caso de fallo de comunicación
- Considera usar `asyncio.open_connection` para sockets asíncronos

### **Testing**

```python
# Ejemplo de test
import asyncio
import aiohttp

async def test_scraper():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000/scrape?url=https://example.com') as resp:
            data = await resp.json()
            assert 'scraping_data' in data
            assert data['status'] == 'success'

asyncio.run(test_scraper())
```

---

¡Éxito con el trabajo práctico! Recuerda comenzar temprano y testear frecuentemente cada componente de forma independiente antes de integrar todo el sistema.

---