import json
from utils import calcular_hash

def verificar_cadena(path_archivo="blockchain.json"):
    try:
        with open(path_archivo, "r") as f:
            cadena = json.load(f)
    except FileNotFoundError:
        print(f"No se encontró el archivo {path_archivo}.")
        return False
    except json.JSONDecodeError:
        print(f"El archivo {path_archivo} contiene JSON inválido.")
        return False

    bloque_anterior_hash = "0" * 64
    corrupciones = []

    for i, bloque in enumerate(cadena):
        ts = bloque["timestamp"]
        datos = bloque["datos"]
        prev_hash = bloque["prev_hash"]
        hash_almacenado = bloque["hash"]

        hash_calculado = calcular_hash(prev_hash, datos, ts)

        if prev_hash != bloque_anterior_hash:
            corrupciones.append(
                (i, "Prev_hash incorrecto", f"Esperado: {bloque_anterior_hash}, Encontrado: {prev_hash}")
            )

        if hash_almacenado != hash_calculado:
            corrupciones.append(
                (i, "Hash incorrecto", f"Calculado: {hash_calculado}, Almacenado: {hash_almacenado}")
            )

        bloque_anterior_hash = hash_almacenado

    if corrupciones:
        print(f"Se detectaron {len(corrupciones)} bloques corruptos:")
        for idx, tipo, detalle in corrupciones:
            print(f"  - Bloque #{idx}: {tipo}. {detalle}")
        return False
    else:
        print(f"La cadena de bloques se verificó correctamente.")
        print(f"Total bloques: {len(cadena)}.")
        return True

if __name__ == "__main__":
    verificar_cadena()
