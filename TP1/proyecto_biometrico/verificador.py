import json
import time
from utils import calcular_hash 
import multiprocessing  
from utils import imprimir_separador
import os

class Verificador:
    def __init__(self, queues, stop_event, lock, output_dir="resultados"):
        self.queues = queues
        self.stop_event = stop_event
        self.resultados_por_timestamp = {}
        self.chain = []
        self.analizadores_terminados = 0
        self.total_analizadores = len(queues)
        self.lock = multiprocessing.Lock() 
        self.output_dir = output_dir

    def guardar_cadena(self):
        with self.lock:
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
            path = os.path.join(self.output_dir, "blockchain.json")
            with open(path, "w") as f:
                json.dump(self.chain, f, indent=4)

    def verificar_alerta(self, freq_media, oxi_media, presion_media):
        if freq_media >= 200:
            return True
        elif not (90 <= oxi_media <= 100):
            return True
        elif presion_media >= 200:
            return True
        else:
            return False

    def verificar(self):
        try:
            while not self.stop_event.is_set():
                for queue in self.queues:
                    while not queue.empty():
                        resultado = queue.get()

                        if resultado is None:
                            self.analizadores_terminados += 1
                            print(f"[VERIFICADOR] 📤 Recibido None de un analizador. Total terminados: {self.analizadores_terminados}")
                            if self.analizadores_terminados == self.total_analizadores:
                                print("[VERIFICADOR] 🛑 Todos los analizadores terminaron. Cerrando verificador.")
                                self.guardar_cadena()
                                return
                            continue

                        ts = resultado["timestamp"]

                        if ts not in self.resultados_por_timestamp:
                            self.resultados_por_timestamp[ts] = {}

                        self.resultados_por_timestamp[ts][resultado["tipo"]] = resultado

                        if len(self.resultados_por_timestamp[ts]) == 3:
                            datos_completos = self.resultados_por_timestamp.pop(ts)

                            frecuencia_media = datos_completos["frecuencia"]["media"]
                            oxigeno_media = datos_completos["oxigeno"]["media"]
                            presion_media = datos_completos["presion"]["media"]

                            alerta = self.verificar_alerta(frecuencia_media, oxigeno_media, presion_media)

                            # Datos necesarios para el hash
                            datos_para_hash = {
                                "frecuencia": {
                                    "media": frecuencia_media,
                                    "desv": datos_completos["frecuencia"]["desv"]
                                },
                                "presion": {
                                    "media": presion_media,
                                    "desv": datos_completos["presion"]["desv"]
                                },
                                "oxigeno": {
                                    "media": oxigeno_media,
                                    "desv": datos_completos["oxigeno"]["desv"]
                                }
                            }

                            with self.lock:
                                prev_hash = self.chain[-1]["hash"] if self.chain else "0" * 64
                                hash_actual = calcular_hash(prev_hash, datos_para_hash, ts)

                                bloque = {
                                    "timestamp": ts,
                                    "datos": datos_para_hash,
                                    "alerta": alerta,
                                    "prev_hash": prev_hash,
                                    "hash": hash_actual
                                }

                                self.chain.append(bloque)

                            self.guardar_cadena()

                            orden_metricas = ["frecuencia", "presion", "oxigeno"]

                            print(f"[VERIFICADOR] 📥 Datos completos para el timestamp ⏱️  {ts}:")

                            for tipo in orden_metricas:
                                info = datos_completos[tipo]
                                print(f"[{tipo.upper()}] 🧪 Valores ventana: {info['ventana']}")

                            for tipo in orden_metricas:
                                info = datos_completos[tipo]
                                print(f"[{tipo.upper()}] 📊 Media: {info['media']:.2f} | Desviación estándar: {info['desv']:.2f}")
                            
                            print(f"[VERIFICADOR] 🚨 Alerta: {alerta}")
                            print(f"[VERIFICADOR] 🧱 Bloque #{len(self.chain)-1} - Hash: {hash_actual}")
                            imprimir_separador()
                            
                time.sleep(0.01)

        except KeyboardInterrupt:
            print("[VERIFICADOR] ⛔ Interrumpido por el usuario. Cerrando proceso.")
            self.guardar_cadena()
