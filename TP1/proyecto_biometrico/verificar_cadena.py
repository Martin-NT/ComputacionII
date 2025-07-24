import json
from utils import calcular_hash
import os

class VerificarCadena:
    def __init__(self, carpeta_resultados="resultados", path_archivo="blockchain.json", path_reporte="reporte.txt"):
        self.carpeta_resultados = carpeta_resultados
        self.path_archivo = os.path.join(carpeta_resultados, path_archivo)
        self.path_reporte = os.path.join(carpeta_resultados, path_reporte)
        self.cadena = []
        self.corrupciones = []

    def cargar_cadena(self):
        try:
            with open(self.path_archivo, "r") as f:
                self.cadena = json.load(f)
            return True
        except FileNotFoundError:
            print(f"--> ❌ No se encontró el archivo 📂 {self.path_archivo}.")
        except json.JSONDecodeError:
            print(f"--> ⚠️ El archivo 📂 {self.path_archivo} contiene JSON inválido.")
        return False

    def verificar_cadena(self):
        bloque_anterior_hash = "0" * 64
        self.corrupciones = []

        for i, bloque in enumerate(self.cadena):
            ts = bloque["timestamp"]
            datos = bloque["datos"]
            prev_hash = bloque["prev_hash"]
            hash_almacenado = bloque["hash"]

            hash_calculado = calcular_hash(bloque_anterior_hash, datos, ts)

            if prev_hash != bloque_anterior_hash:
                self.corrupciones.append(
                    (i, "🔗 Prev_hash incorrecto", f"Esperado: {bloque_anterior_hash}, Encontrado: {prev_hash}")
                )

            if hash_almacenado != hash_calculado:
                self.corrupciones.append(
                    (i, "🧮 Hash incorrecto", f"Calculado: {hash_calculado}, Almacenado: {hash_almacenado}")
                )

            bloque_anterior_hash = hash_almacenado

        return len(self.corrupciones) == 0


    def generar_reporte(self):
        # Crea carpeta si no existe
        if not os.path.exists(self.carpeta_resultados):
            os.makedirs(self.carpeta_resultados)
            
        total_bloques = len(self.cadena)
        bloques_con_alerta = 0

        suma_frecuencia = 0.0
        suma_presion = 0.0
        suma_oxigeno = 0.0

        for bloque in self.cadena:
            if bloque.get("alerta"):
                bloques_con_alerta += 1

            datos = bloque.get("datos", {})

            frecuencia_media = datos.get("frecuencia", {}).get("media", 0)
            presion_media = datos.get("presion", {}).get("media", 0)
            oxigeno_media = datos.get("oxigeno", {}).get("media", 0)

            suma_frecuencia += float(frecuencia_media)
            suma_presion += float(presion_media)
            suma_oxigeno += float(oxigeno_media)

        if total_bloques > 0:
            promedio_frecuencia = suma_frecuencia / total_bloques
            promedio_presion = suma_presion / total_bloques
            promedio_oxigeno = suma_oxigeno / total_bloques
        else:
            promedio_frecuencia = promedio_presion = promedio_oxigeno = 0

        reporte = (
            "=======================================================================\n"
            "                  Reporte Final - Cadena Biométrica\n"
            "=======================================================================\n\n"
            f"Cantidad total de bloques    : {total_bloques}\n"
            f"Número de bloques con alertas: {bloques_con_alerta}\n\n"
            "Promedios generales:\n"
            f"  - Frecuencia cardíaca (bpm) : {promedio_frecuencia:.2f}\n"
            f"  - Presión sistólica (mmHg)  : {promedio_presion:.2f}\n"
            f"  - Nivel de oxígeno (%)      : {promedio_oxigeno:.2f}\n\n"
            "=======================================================================\n"
            "Estado: Cadena verificada sin errores\n"
            "=======================================================================\n"
        )

        with open(self.path_reporte, "w") as f:
            f.write(reporte)

    def ejecutar(self):
        if not self.cargar_cadena():
            return False

        if not self.verificar_cadena():
            print(f"--> ❌ Se detectaron {len(self.corrupciones)} bloques corruptos:")
            for idx, tipo, detalle in self.corrupciones:
                print(f"  - ❗ Bloque #{idx}: {tipo}. {detalle}")
            print("\n--> 🛑 No se generará reporte porque la cadena no pasó la verificación.")

            return False

        print(f"--> ✅ La cadena de bloques se verificó correctamente.")
        print(f"--> 📦 Total bloques: {len(self.cadena)}.")
        self.generar_reporte()
        print(f"--> 📝 Reporte generado correctamente en {self.path_reporte}")
        return True


if __name__ == "__main__":
    verificador = VerificarCadena()
    verificador.ejecutar()
