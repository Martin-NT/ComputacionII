import hashlib
import json
import time
from utils import calcular_hash 

class Verificador:
    def __init__(self, queues, stop_event):
        self.queues = queues
        self.stop_event = stop_event
        self.resultados_por_timestamp = {}
        self.chain = []  # Cadena de bloques en memoria
        self.analizadores_terminados = 0
        self.total_analizadores = len(queues)

    def guardar_cadena(self):
        with open("blockchain.json", "w") as f:
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

                        # Detectar mensaje de cierre (None)
                        if resultado is None:
                            self.analizadores_terminados += 1
                            print(f"[VERIFICADOR] Recibido None de un analizador. Total terminados: {self.analizadores_terminados}")
                            if self.analizadores_terminados == self.total_analizadores:
                                print("[VERIFICADOR] Todos los analizadores terminaron. Cerrando verificador.")
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
                            
                            prev_hash = self.chain[-1]["hash"] if self.chain else "0"*64
                            hash_actual = calcular_hash(prev_hash, datos_completos, ts)
                            
                            bloque = {
                                "timestamp": ts,
                                "datos": datos_completos,
                                "alerta": alerta,
                                "prev_hash": prev_hash,
                                "hash": hash_actual
                            }

                            self.chain.append(bloque)
                            self.guardar_cadena()

                            print(f"[VERIFICADOR] Datos completos para el timestamp {ts}: \n{datos_completos}")
                            print(f"[VERIFICADOR] Alerta: {alerta}")
                            print(f"[VERIFICADOR] Bloque #{len(self.chain)-1} - Hash: {hash_actual} - Alerta: {alerta}")

                time.sleep(0.1)  # evitar bucle ocupado

        except KeyboardInterrupt:
            print("[VERIFICADOR] Interrumpido por el usuario. Cerrando proceso.")
            self.guardar_cadena()
