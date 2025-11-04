# Conversión entre JSON ↔ bytes y soporte opcional para Pickle.
from __future__ import annotations
import json
import pickle
from typing import Any

def to_json(data: Any) -> bytes:
    """
    Convierte un objeto Python (dict, lista, etc.) a bytes JSON UTF-8.
    Compacta la salida eliminando espacios innecesarios.
    """
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

def from_json(raw: bytes) -> Any:
    """
    Decodifica bytes UTF-8 que contienen JSON y devuelve el objeto Python.
    """
    return json.loads(raw.decode("utf-8"))

def to_pickle(data: Any) -> bytes:
    """
    Serializa cualquier objeto Python a bytes binarios (pickle).
    Útil para mensajes internos si no se necesita legibilidad.
    """
    return pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)

def from_pickle(raw: bytes) -> Any:
    """
    Deserializa bytes binarios generados con pickle.
    """
    return pickle.loads(raw)
