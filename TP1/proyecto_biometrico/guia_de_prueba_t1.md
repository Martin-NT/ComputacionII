# Guía de Prueba - Tarea 1

Este documento explica cómo probar el sistema actual correspondiente a la **Tarea 1** del Trabajo Práctico: *"Sistema Concurrente de Análisis Biométrico con Cadena de Bloques Local"*.

---

## ✅ Requisitos Previos

* Python 3.9 o superior
* Entorno virtual creado y activado
* Archivos implementados:

  * `main.py`
  * `generador.py`
  * `analizador.py`
  * `verificador.py`

---

## ▶️ Cómo Ejecutar el Programa

1. **Activar entorno virtual**:

   ```bash
   source venv/bin/activate
   ```

2. **Ejecutar el script principal**:

   ```bash
   python3 main.py
   ```

---

## 🔍 Comportamiento Esperado

Cada segundo:

* Se genera un dato biométrico con:

  * `frecuencia`: int(60-180)
  * `presion`: \[int(110-180), int(70-110)] (sistólica/diastólica)
  * `oxigeno`: int(90-100)
* Se imprime:

  * `[MAIN] Enviado dato: {...}`
  * `[FRECUENCIA]`, `[PRESION]`, `[OXIGENO]`: valor actual, media y desviación estándar.
  * `[VERIFICADOR] Recibido`: diccionario con resultados enviados por analizadores.

### Ejemplo:

```
[MAIN] Enviado dato: {'timestamp': '2025-07-15T19:12:41.615753', 'frecuencia': 115, 'presion': [180, 88], 'oxigeno': 96}
[FRECUENCIA] Valor: 115 | Media: 115.00 | Desviación estándar: 0.00
[PRESION] Valor: 180 | Media: 180.00 | Desviación estándar: 0.00
[OXIGENO] Valor: 96 | Media: 96.00 | Desviación estándar: 0.00
[VERIFICADOR] Recibido: {...}
```

---

## ⛔️ Detener la Ejecución

* Presioná `Ctrl + C` para interrumpir.
* Verás mensajes indicando que los procesos se cierran correctamente:

```
Interrumpido por el usuario.
[FRECUENCIA] Analizador interrumpido. Cerrando proceso.
[OXIGENO] Analizador interrumpido. Cerrando proceso.
[VERIFICADOR] Interrumpido por el usuario. Cerrando proceso.
```

---

## 📂 Archivos Esperados

* `main.py`
* `generador.py`
* `analizador.py`
* `verificador.py`
* `venv/`

*Aún no se genera `blockchain.json`, ya que pertenece a la Tarea 2.*



## ⚖️ Verificación Manual de Cálculos

Para asegurarte de que se calcula correctamente la media y desviación, agregá esto en `analizador.py`:

```python
print(f"[{tipo.upper()}] Valores recientes: {valores_obtenidos}")
```

### ¿Qué es `valores_obtenidos`?

Es la **ventana móvil** de los últimos 30 segundos de valores numéricos (por tipo). Se va actualizando con cada nuevo dato y permite calcular estadísticas sobre las muestras más recientes sin tener en cuenta valores antiguos.

---

## 🚀 Siguiente Paso

Implementar la **Tarea 2**, que incluye:

* Validación de los resultados.
* Construcción de bloques con hash SHA-256.
* Escritura en `blockchain.json`.
