
# TP1 - Sistema Concurrente de Análisis Biométrico con Cadena de Bloques Local

## Información   
- **Nombre:** Martin Navarro
- **Legajo:** 62181
- **Correo:** mt.navarro@alumno.um.edu.ar
- **Materia**: Computación 2

## Descripción

Trabajo práctico de la materia Computación 2. El objetivo es construir un sistema concurrente y distribuido en procesos, que genere, procese y almacene datos biométricos en una cadena de bloques local.

---

## 📁 Estructura del Proyecto

| Archivo | Descripción |
|--------|-------------|
| `main.py` | Inicia y coordina todos los procesos del sistema. |
| `generador.py` | Genera datos biométricos (frecuencia cardíaca, presión arterial y oxígeno). |
| `analizador.py` | Procesa cada tipo de dato (uno por proceso) y calcula estadísticas. |
| `verificador.py` | Espera resultados de los analizadores y genera bloques con alertas. |
| `verificar_cadena.py` | Verifica la integridad de la cadena de bloques y genera un `reporte.txt`. |
| `utils.py` | Funciones auxiliares compartidas (hash, manejo de tiempo, validación, etc.). |
| `blockchain.json` | Archivo persistente que guarda la cadena de bloques generada. |
| `reporte.txt` | Reporte final con resumen de alertas y estado de verificación. |
| `requirements.txt` | Lista de dependencias necesarias (por ahora solo `numpy`). |
| `.gitignore` | Archivos y carpetas excluidos del repositorio (ej: `env/`, `__pycache__/`). |
| `README.md` | Este archivo con toda la información del proyecto. |

---

## 📦 Requisitos

- Python 3.9 o superior
- (Recomendado) Uso de entorno virtual
- Dependencias definidas en `requirements.txt`
- Módulos estándar utilizados:
  - `multiprocessing`, `queue`, `json`, `datetime`, `random`, `hashlib`, `os`, `time`
- Comunicación entre procesos con:
  - `Pipe` y `Queue`
- Sincronización con:
  - `Lock`, `Semaphore`, `Event`
- El programa debe finalizar limpiamente, sin dejar procesos zombies ni recursos abiertos.

---

## ⚙️ Comandos de Intalación y Ejecución

### 🧪 Instalación

1. Clonar el repositorio
```bash
git clone git@github.com:Martin-NT/ComputacionII.git
```

2. Ubicarse en el proyecto
```bash
cd ComputacionII/TP1/proyecto_biometrico
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

### ▶️ Ejecución

6. Ejecutar el sistema principal
```bash
python3 main.py
```
7. Verificar integridad de la cadena
```bash
python3 verificar_cadena.py
```

### 🔍 Verificación de Procesos
8. Para asegurarte de que no quedan procesos zombies o huérfanos en otra terminal:
```bash
ps aux | grep Z
```
```bash
ps -el | grep Z
```

## ✅ Resultado Esperado
- Se genera un archivo blockchain.json con los bloques generados por el sistema.
- Al ejecutar verificar_cadena.py, se analiza la integridad de la cadena y se crea reporte.txt con estadísticas de alertas, errores y validación.
- Todos los procesos finalizan correctamente al presionar Ctrl+C o cuando finaliza el proceso, sin dejar procesos zombies ni recursos colgados.

---

## Documentación de Archivos

### generador.py

Este módulo contiene la clase `GeneradorBiometrico`, responsable de generar datos biométricos simulados.

- **Clase `GeneradorBiometrico`**:  
  - **Método `generar_dato()`**:  
    - Genera y devuelve un diccionario con un timestamp actual y valores aleatorios para:  
      - `frecuencia` (60 a 180 bpm)  
      - `presion` (presión sistólica entre 110 y 180, presión diastólica entre 70 y 110)  
      - `oxigeno` (nivel de oxígeno entre 90 y 100 %)  

---

### analizador.py

Este módulo define la clase `Analizador` que procesa datos biométricos recibidos desde un proceso generador, calcula estadísticas y envía resultados a un proceso verificador.

- **Clase `Analizador`**:  
  - **Atributos**:  
    - `tipo`: indica el tipo de dato biométrico que analiza (`frecuencia`, `presion` o `oxigeno`).  
    - `conn`: extremo del pipe para recibir datos.  
    - `verificador_queue`: cola para enviar resultados al verificador.  
    - `stop_event`: evento para detener el análisis.  
    - `semaphore`: controla la concurrencia permitiendo máximo 2 analizadores activos simultáneamente.  
    - `valores_obtenidos`: lista con los últimos 30 valores analizados para cálculo estadístico.  

  - **Método `analizar()`**:  
    - En un bucle hasta que se setea `stop_event`, lee datos si están disponibles sin bloqueo.  
    - Extrae el valor correcto según tipo (`frecuencia`, `presion` o `oxigeno`).  
    - Calcula la media y desviación estándar de los últimos 30 valores.  
    - Envía un diccionario con tipo, timestamp, media y desviación a la cola del verificador con control de concurrencia (semaphore).  
    - Envía `None` a la cola cuando termina para indicar cierre.  

- **Función `ejecutar_analizador()`**:  
  - Instancia un `Analizador` y llama a su método `analizar()`.  

### verificador.py

Este módulo implementa el proceso **Verificador**, responsable de recolectar los resultados enviados por los analizadores, detectar alertas y construir la cadena de bloques en el archivo `blockchain.json`.

---

- **Clase `Verificador`**

  - **Constructor** `__init__(queues, stop_event, lock)`  
    - `queues`: lista de `multiprocessing.Queue` con resultados provenientes de los analizadores (`frecuencia`, `presion`, `oxigeno`).  
    - `stop_event`: evento compartido que permite indicar cuándo detener el proceso.  
    - `lock`: utilizado para sincronizar el acceso concurrente al archivo `blockchain.json` y evitar condiciones de carrera.  

---

- **Método `verificar()`**  
  - Bucle principal que recoge los datos desde las colas de los analizadores.  
  - Agrupa los resultados por `timestamp` hasta obtener los tres tipos requeridos.  
  - Una vez que hay datos completos:
    - Calcula si hay una **alerta biométrica** en base a los siguientes criterios:
      - Frecuencia ≥ 200
      - Oxígeno fuera del rango [90, 100]
      - Presión ≥ 200
    - Construye un nuevo bloque con:
      - `timestamp`
      - `datos`: diccionario con `media` y `desv` de cada parámetro
      - `alerta`: `True` o `False`
      - `prev_hash`: hash del bloque anterior (o `"0"*64` si es el primero)
      - `hash`: generado con `utils.calcular_hash(prev_hash, datos, timestamp)`
    - Agrega el bloque a la cadena (`self.chain`) y lo guarda en `blockchain.json`.  
  - El verificador termina cuando los tres analizadores envían una señal de finalización (`None`).

---

- **Método `guardar_cadena()`**  
  - Escribe el contenido actual de la cadena (`self.chain`) en el archivo `blockchain.json` con formato legible (`indent=4`).
  - Se utiliza un `lock` para evitar conflictos si varios procesos intentan escribir al mismo tiempo.

---

- **Método `verificar_alerta(frecuencia, oxigeno, presion)`**  
  - Devuelve `True` si alguno de los valores excede los umbrales definidos.  
  - En caso contrario, devuelve `False`.

---

### main.py

Este script principal orquesta el sistema concurrente de análisis biométrico.

- Crea un generador de datos biométricos.  
- Establece pipes para comunicación entre el generador y los analizadores.  
- Crea colas para que los analizadores envíen resultados al verificador.  
- Define un evento, un lock y un semáforo para sincronización y control de concurrencia.  
- Crea y arranca procesos para tres analizadores (`frecuencia`, `presion`, `oxigeno`) y un proceso verificador.  
- En un ciclo de 60 iteraciones, genera datos y los envía a cada analizador una vez por segundo.  
- Captura interrupciones para detener los procesos limpiamente y asegurar cierre sin procesos zombies.  

---

### utils.py

Contiene funciones utilitarias para el sistema.

- **Función `calcular_hash(prev_hash, datos, timestamp)`**:  
  - Recibe el hash previo, los datos y el timestamp del bloque.  
  - Serializa los datos con claves ordenadas y sin espacios extra.  
  - Concadena `prev_hash + datos_serializados + timestamp`.  
  - Calcula y devuelve el hash SHA-256 de la concatenación.  

---

### verificar_cadena.py

Este módulo verifica la integridad de la cadena de bloques biométrica y genera un reporte con estadísticas.

- **Clase `VerificarCadena`**:  
  - **Atributos**:  
    - `path_archivo`: ruta al archivo JSON de la cadena (`blockchain.json`).  
    - `path_reporte`: ruta al archivo de reporte (`reporte.txt`).  
    - `cadena`: lista con los bloques cargados.  
    - `corrupciones`: lista con errores encontrados durante la verificación.  

  - **Método `cargar_cadena()`**:  
    - Intenta cargar la cadena desde archivo JSON.  
    - Maneja errores si el archivo no existe o tiene formato inválido.  

  - **Método `verificar_cadena()`**:  
    - Recorre cada bloque y verifica que:  
      - El `prev_hash` coincide con el hash del bloque anterior.  
      - El hash almacenado coincide con el hash recalculado.  
    - Registra en `corrupciones` cualquier inconsistencia.  

  - **Método `generar_reporte()`**:  
    - Calcula estadísticas generales: total bloques, bloques con alertas y promedio de frecuencia, presión y oxígeno.  
    - Escribe un reporte formateado con estos datos.  

  - **Método `ejecutar()`**:  
    - Ejecuta todo el flujo: carga la cadena, verifica integridad y genera reporte si todo es correcto.  
    - Informa al usuario sobre errores o éxito.  

- Puede ejecutarse directamente con `python3 verificar_cadena.py`.  

---

## Resultado esperado

- Se genera un archivo `blockchain.json` con los bloques biométricos.  
- Al ejecutar `verificar_cadena.py`, se analiza la integridad y se crea `reporte.txt` con estadísticas y alertas.  
- Todos los procesos terminan correctamente al presionar Ctrl+C, sin dejar procesos zombies o huérfanos.

---
