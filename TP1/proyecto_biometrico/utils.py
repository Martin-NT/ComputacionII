import hashlib
import json

def calcular_hash(prev_hash, datos, timestamp):
    # Serializar datos consistentemente: claves ordenadas, sin espacios extra
    datos_serializados = json.dumps(datos, sort_keys=True, separators=(',', ':'))
    to_hash = prev_hash + datos_serializados + timestamp
    return hashlib.sha256(to_hash.encode()).hexdigest()

def imprimir_separador():
    print("\n" + "🧱" * 40 + "\n")
