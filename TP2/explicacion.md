# TP2 
Este documento explica qué hace cada archivo del proyecto.
---

## 1) Mapa general del proyecto

```
TP2/
├── server_scraping.py          # Servidor HTTP asíncrono (Parte A)
├── server_processing.py        # (Stub opcional) Servidor B de prueba
├── scraper/
│   ├── __init__.py             # Marca paquete
│   ├── async_http.py           # Descarga de HTML asíncrona (aiohttp)
│   ├── html_parser.py          # Parsing de título, links, headers, imágenes
│   └── metadata_extractor.py   # Extracción de metatags relevantes
├── common/
│   ├── __init__.py             # Marca paquete
│   └── serialization.py        # Helpers JSON (bytes <-> dict)
├── requirements.txt            # Dependencias
└── README.md                   # Instrucciones rápidas de uso
```

**Idea clave:** el cliente habla con **server_scraping.py**, que coordina el scraping y (si está disponible) le pide trabajo al servidor B. La Parte A ya funciona independientemente; la integración con B es asíncrona y transparente para el cliente.

---

## 2) Flujo de una request (de punta a punta)

1. **Cliente** llama: `GET /scrape?url=https://example.com`.
2. **`server_scraping.py`** recibe la request con `aiohttp.web`.
3. Lanza una **tarea asíncrona** para descargar el HTML (`fetch_text`) y, en paralelo, prepara la llamada asíncrona al servidor B (si está corriendo).
4. Cuando llega el HTML, usa **`html_parser.py`** y **`metadata_extractor.py`** para extraer: título, links, headers H1–H6, cantidad de imágenes y metatags.
5. Espera el resultado de B (si existe) **sin bloquear**.
6. Responde al cliente con **un JSON consolidado**: `scraping_data` + `processing_data` (si B respondió).

Diagrama rápido:

```
Cliente → server_scraping.py → (tarea A) fetch_text
                         ↘→ (tarea B) llamada a Servidor B (opcional)
parse_html + extract_meta → unir resultados → JSON al Cliente
```

---

## 3) Detalle de archivos

### 3.1 `server_scraping.py` (núcleo de la Parte A)

**Rol:** Servidor HTTP asíncrono. Expone `/scrape`, coordina tareas, encapsula errores y arma el JSON final.

**Lo más importante dentro del archivo:**

* **Imports clave:** `argparse`, `asyncio`, `aiohttp.web`, y módulos propios (`scraper/*`, `common/serialization`).
* **Handlers asíncronos (`async def`)**: `handle_scrape(request)` procesa la query `url`, lanza tareas asíncronas (descarga y llamada a B), hace `await` cuando necesita datos y retorna `web.json_response(...)`.
* **Comunicación con B (asíncrona):** usa `asyncio.open_connection` para abrir un socket TCP y un **protocolo de longitud-prefijo + JSON** (4 bytes big-endian con la longitud, seguido por el JSON). Así evita leer de más o quedarse corto con `recv`.
* **CLI (`argparse`)**: permite correr con `--ip`, `--port`, `--proc-ip`, `--proc-port`.
* **Manejo de errores**: responde 400 (URL faltante), 504 (timeout) o 500 (excepciones generales), siempre en **JSON**.

**Por qué es asíncrono:** `aiohttp` y `asyncio` permiten que el servidor atienda **muchas conexiones concurrentes** sin crear un hilo por conexión y sin bloquear cuando espera red/IO.

---

### 3.2 `scraper/async_http.py`

**Rol:** Descarga **asíncrona** del HTML.

**Claves técnicas:**

* `aiohttp.ClientSession` con **timeout** (30s) y `User-Agent` propio.
* `resp.raise_for_status()` levanta errores HTTP 4xx/5xx para que el servidor devuelva una respuesta clara.
* `await resp.text()` decodifica el cuerpo según el `Content-Type`/encoding informado por el servidor.

**Cuándo tocarlo:** si necesitás headers custom, cookies, autenticación o limitar redirecciones.

---

### 3.3 `scraper/html_parser.py`

**Rol:** A partir del HTML, extraer **título**, **todos los links** (normalizados a URLs absolutas con `urljoin`), **estructura** (conteo de `h1..h6`) y **cantidad de imágenes**.

**Claves técnicas:**

* Usa `BeautifulSoup` con parser `lxml` (rápido y tolerante).
* Normaliza links relativos → absolutos con `urljoin(base_url, href)`. Esto es crítico para análisis posterior y evita duplicados relativos.
* Devuelve un `dict` listo para serializar a JSON.

**Cuándo tocarlo:** si querés extraer más cosas (p.ej., links externos vs internos, textos de los headers, etc.).

---

### 3.4 `scraper/metadata_extractor.py`

**Rol:** Extraer **metatags relevantes**: `description`, `keywords`, y **Open Graph** (`og:title`, `og:description`, `og:image`).

**Claves técnicas:**

* Busca `meta` con `name` o `property` y toma el `content` si no está vacío.
* Filtra por un conjunto `RELEVANT_META` para no ensuciar el JSON.

**Cuándo tocarlo:** si la consigna pide más metatags (Twitter Cards, `author`, etc.).

---

### 3.5 `common/serialization.py`

**Rol:** Helpers mínimos para convertir entre **dict ↔ bytes** usando JSON UTF‑8.

**Claves técnicas:**

* `to_json(data) -> bytes`: `json.dumps(...).encode("utf-8")`.
* `from_json(raw: bytes) -> Any`: `json.loads(raw.decode("utf-8"))`.

**Por qué existe:** el protocolo con B es **binario** (lleva un prefijo de longitud de 4 bytes). Necesitamos manipular **bytes**, no sólo strings.

---

### 3.6 `server_processing.py` (stub opcional para pruebas)

**Rol:** Un servidor B **mínimo** de prueba. Permite que la Parte A haga la llamada y reciba un `processing_data` inventado.

**Claves técnicas:**

* Usa `socketserver` y un handler que **lee** un mensaje con longitud-prefijo, **parsea** JSON y **responde** con otro JSON empacado igual.
* Es sólo para que puedas probar la coordinación A↔B. En la Parte B real implementaremos mediciones y procesamiento de imágenes.

---

## 4) Conceptos asíncronos que estás usando

* **Event loop (`asyncio`)**: un ciclo que agenda y ejecuta tareas cooperativas. Cuando una tarea espera I/O, cede el control, y otras tareas pueden avanzar.
* **`async def` / `await`**: funciones asíncronas y puntos de suspensión. `await` **no bloquea**; permite que el loop ejecute otras tareas mientras espera.
* **`aiohttp.web`**: framework HTTP asíncrono. Cada request entra a un `handler` `async`, que puede `await` operaciones de red.
* **`asyncio.create_task(...)`**: lanza una corrutina para que corra **en paralelo** (concurrencia cooperativa) dentro del mismo loop.
* **Sockets asíncronos (`asyncio.open_connection`)**: crean `StreamReader/StreamWriter` no bloqueantes para protocolos propios.

---

## 5) Protocolo A↔B (longitud-prefijo + JSON)

**Motivación:** con sockets, no sabés cuántos bytes te llegarán por `read`. Para encuadrar mensajes, mandamos primero **4 bytes big-endian** con la longitud del JSON, y luego el **JSON en bytes**.

**Enviar:** `len(payload).to_bytes(4, "big") + payload`

**Recibir:**

1. Leer 4 bytes → convertir a `int` (longitud).
2. Leer exactamente `longitud` bytes.
3. Decodificar con `from_json`.

Esto evita concatenaciones o cortes de mensajes.

---

## 6) Errores típicos y cómo reconocerlos

* **`HTTP 4xx/5xx`**: `resp.raise_for_status()` lanza `ClientResponseError`. El servidor A devuelve 502 con el código original.
* **Timeouts**: si el sitio tarda mucho, captura `asyncio.TimeoutError` y responde **504**.
* **URL inválida**: `aiohttp` puede lanzar `InvalidURL`. El handler lo atrapará como excepción genérica → **500** con el mensaje.
* **Servidor B caído**: la tarea hacia B fallará; el handler devuelve igual `scraping_data` y `processing_data` vacío.

---

## 7) Preguntas guía

1. ¿Por qué `await` **no bloquea** el servidor y `time.sleep()` sí lo haría?
2. ¿Qué ventajas trae `ClientSession` en `aiohttp` frente a `requests` tradicional?
3. ¿Por qué conviene normalizar los links con `urljoin`? Da un ejemplo de URL relativa.
4. ¿Cómo sabés que no se mezclan mensajes cuando A habla con B?
5. ¿Qué responde el servidor ante `GET /scrape` **sin** `?url=`?
6. Si el HTML no tiene `<title>`, ¿qué devuelve el parser? ¿Por qué es robusto?

---

## 8) Comandos útiles

* Instalar deps: `pip install -r requirements.txt`
* Levantar A: `python server_scraping.py -i 0.0.0.0 -p 8000 --proc-ip 127.0.0.1 --proc-port 9090`
* Levantar B (stub): `python server_processing.py -i 127.0.0.1 -p 9090 -n 0`
* Probar: `curl "http://localhost:8000/scrape?url=https://example.com"`

---

## 9) Próximos pasos (para la Parte B)

* Implementar medición de performance real (tiempos, tamaños y cantidad de requests).
* Descargar 2–3 imágenes y generar **thumbnails** con Pillow (base64).
* Preparar **screenshot** en headless (Selenium/Playwright) activable por flag.

> Con esta guía, deberías poder explicar file-by-file qué hace cada parte del sistema, cómo fluye una request y qué gana el diseño asíncrono en concurrencia y claridad.
