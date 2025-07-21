class Verificador:
    def __init__(self, conn):
        self.conn = conn
        self.resultados_por_timestamp = {}

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
            while True:
                try:
                    resultado = self.conn.recv()
                except EOFError:
                    print("[VERIFICADOR] Pipe cerrado. Cerrando verificador.")
                    break

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

                    print(f"[VERIFICADOR] Datos completos para el timestamp {ts}: \n{datos_completos}")
                    print(f"[VERIFICADOR] Alerta: {alerta}")

        except KeyboardInterrupt:
            print("[VERIFICADOR] Interrumpido por el usuario. Cerrando proceso.")
        finally:
            self.conn.close()
