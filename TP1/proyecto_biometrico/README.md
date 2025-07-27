
# TP1 - Sistema Concurrente de Análisis Biométrico con Cadena de Bloques Local

## Información   
- **Nombre:** Martin Navarro
- **Legajo:** 62181
- **Correo:** mt.navarro@alumno.um.edu.ar
- **Materia**: Computación II

## Descripción

Trabajo práctico de la materia Computación II. El objetivo es construir un sistema concurrente y distribuido en procesos, que genere, procese y almacene datos biométricos en una cadena de bloques local.

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
- Instalar dependencias definidas en `requirements.txt` (Paso 5 de Instalación) 
- Módulos estándar utilizados:
  - `multiprocessing`, `queue`, `json`, `datetime`, `random`, `hashlib`, `os`, `time`
- Comunicación entre procesos con:
  - `Pipe` y `Queue`
- Sincronización con:
  - `Lock`, `Semaphore`, `Event`
- El programa debe finalizar limpiamente, sin dejar procesos zombies ni recursos abiertos.

---

## Documentación de Archivos

### generador.py

Este módulo contiene la clase GeneradorBiometrico, responsable de simular la generación de datos biométricos.

- **Clase `GeneradorBiometrico`**
  - **Método `generar_dato()`**
    - Devuelve un diccionario con:
      - `timestamp`: fecha y hora actual.
      - `frecuencia`: valor aleatorio entre 60 y 180 (latidos por minuto).
      - `presion`: tupla con presión sistólica (110–180) y diastólica (70–110).
      - `oxigeno`: valor aleatorio entre 90% y 100%.
---

### analizador.py

Define la clase `Analizador`, utilizada por cada proceso para analizar una métrica biométrica en tiempo real (frecuencia, presión u oxígeno).

- **Clase `Analizador`**
  - **Atributos**:
    - `tipo`: tipo de dato a analizar (`frecuencia`, `presion`, `oxigeno`).
    - `conn`: conexión del `Pipe` por donde recibe datos desde el generador.
    - `verificador_queue`: `Queue` hacia el verificador para enviar estadísticas calculadas.
    - `stop_event`: evento compartido para indicar cuándo detener el análisis.
    - `semaphore`: semáforo para limitar el número de analizadores concurrentes.
    - `valores_obtenidos`: ventana deslizante de los últimos 30 valores para cálculo estadístico.

  - **Método `analizar()`**
    - Escucha continuamente la conexión (`conn`) y acumula los últimos 30 valores.
    - Calcula la media y desviación estándar con `numpy`.
    - Envia al verificador un diccionario con:
      ```python
      {
        "tipo": "frecuencia/presion/oxigeno",
        "timestamp": "...",
        "media": valor,
        "desv": valor,
        "ventana": [últimos 30 valores]
      }
      ```
    - Utiliza `semaphore` para controlar el acceso a la `Queue`.
    - Al finalizar, envía `None` para indicar el fin del análisis.

- **Función `ejecutar_analizador()`**
  - Crea un analizador y llama al método `analizar()`.

---

### verificador.py

Contiene el proceso `Verificador`, que escucha las métricas analizadas, verifica condiciones de alerta, construye bloques de datos y los guarda en una cadena de bloques persistente (`blockchain.json`).

- **Clase `Verificador`**
  - **Constructor `__init__(queues, stop_event, lock, output_dir="resultados")`**
    - `queues`: lista de colas con resultados desde los analizadores.
    - `stop_event`: evento para detener el bucle de verificación.
    - `lock`: `multiprocessing.Lock` para sincronizar acceso a archivos.
    - `output_dir`: carpeta donde se guarda la cadena (`blockchain.json`).

  - **Método `verificar()`**
    - Escucha resultados desde las tres colas hasta recibir los tres tipos (`frecuencia`, `presion`, `oxigeno`) para cada `timestamp`.
    - Verifica si hay alerta:
      - Frecuencia ≥ 200.
      - Presión sistólica ≥ 200.
      - Oxígeno fuera del rango [90–100].
    - Construye un bloque con:
      ```python
      {
        "timestamp": ...,
        "datos": {
            "frecuencia": {"media": ..., "desv": ...},
            "presion": {"media": ..., "desv": ...},
            "oxigeno": {"media": ..., "desv": ...}
        },
        "alerta": True/False,
        "prev_hash": ...,
        "hash": ...
      }
      ```
    - Agrega el bloque a `self.chain` y lo guarda en `blockchain.json`.
    - Imprime resumen del bloque por consola.
    - Termina cuando los tres analizadores envían `None`.

  - **Método `guardar_cadena()`**
    - Guarda la cadena de bloques en `blockchain.json` con formato indentado.
    - Usa `lock` para evitar escritura concurrente.

  - **Método `verificar_alerta()`**
    - Evalúa si alguna de las tres métricas biométricas está fuera del rango normal.
---

### main.py

Script principal que coordina todos los procesos del sistema.

- Crea el generador de datos biométricos.
- Configura:
  - Tres `Pipe` para comunicación con los analizadores.
  - Tres `Queue` para enviar estadísticas al verificador.
  - `stop_event` para coordinación de finalización.
  - `semaphore` que limita la ejecución simultánea a 2 analizadores.
- Lanza:
  - Tres procesos para los analizadores (frecuencia, presión, oxígeno).
  - Un proceso verificador.
- En un ciclo de 60 iteraciones (1 por segundo):
  - Genera un dato biométrico y lo envía por los tres pipes.
- Al finalizar:
  - Envía `None` a los analizadores para señal de término.
  - Cierra todos los pipes y espera que los procesos finalicen.
  - Asegura que no queden procesos zombies ni recursos abiertos.

---

### utils.py

Funciones auxiliares del sistema.

- **`calcular_hash(prev_hash, datos, timestamp)`**
  - Serializa los `datos` ordenadamente (sin espacios extra).
  - Concatena con el `prev_hash` y el `timestamp`.
  - Devuelve el hash SHA-256 del resultado.

- **`imprimir_separador()`**
  - Imprime un separador visual de bloques con emojis 🧱.
---

### verificar_cadena.py

Verifica la integridad de la cadena de bloques (`blockchain.json`) y genera un reporte (`reporte.txt`) con estadísticas generales.

- **Clase `VerificarCadena`**
  - **Atributos**:
    - `cadena`: lista de bloques cargados.
    - `corrupciones`: errores detectados en la cadena.
    - Rutas a `blockchain.json` y `reporte.txt`.

  - **Método `cargar_cadena()`**
    - Carga el archivo `blockchain.json`.
    - Reporta error si no existe o tiene formato inválido.

  - **Método `verificar_cadena()`**
    - Recalcula los hashes de todos los bloques.
    - Verifica que:
      - Cada `prev_hash` coincida con el hash del bloque anterior.
      - El `hash` almacenado coincida con el recalculado.
    - Si encuentra errores, los guarda en `corrupciones`.

  - **Método `generar_reporte()`**
    - Calcula:
      - Total de bloques.
      - Cantidad de alertas.
      - Promedios generales de frecuencia, presión y oxígeno.
    - Escribe `reporte.txt` con formato legible y resumen final.

  - **Método `ejecutar()`**
    - Ejecuta todo el flujo: carga, verifica e informa resultado.
    - Solo genera el reporte si la cadena está libre de errores.

- Puede ejecutarse directamente con `python3 verificar_cadena.py`.  

---

## ✅ Resultado Esperado

- Se genera un archivo blockchain.json con los bloques generados por el sistema.
- Al ejecutar verificar_cadena.py, se analiza la integridad de la cadena y se crea reporte.txt con estadísticas de alertas, errores y validación.
- Todos los procesos finalizan correctamente al presionar Ctrl+C o cuando finaliza el proceso, sin dejar procesos zombies ni recursos colgados.

---

## 🔄 Elección de `Pipe` sobre FIFO

En este proyecto se utilizó `Pipe` (de `multiprocessing`) en lugar de FIFO (archivos especiales) para la comunicación entre procesos por las siguientes razones:

- `Pipe` es **una solución de comunicación en memoria** directamente integrada en Python, lo que permite una transmisión de datos **más rápida y eficiente** entre procesos relacionados (padre-hijo).
- Es más **seguro y manejable** que un FIFO, ya que:
  - No requiere crear ni borrar archivos en el sistema de archivos.
  - No hay riesgo de interferencia externa (otro proceso podría escribir en un FIFO si conoce su ruta).
- `Pipe` proporciona **extremos de lectura y escritura directamente en memoria**, ideales para la comunicación entre procesos que están bajo nuestro control.
- El uso de `Pipe` es **más simple y directo** que manejar un FIFO con `os.mkfifo()` y abrir archivos manualmente.

En este sistema, el generador de datos es el **único escritor**, y cada analizador es el **único lector** de su `Pipe`. Esto hace que la estructura de `Pipe` sea adecuada y eficiente.

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
