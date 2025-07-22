import numpy as np

class Analizador:
    def __init__(self, tipo, conn, verificador_queue, stop_event):
        self.tipo = tipo
        self.conn = conn
        self.verificador_queue = verificador_queue
        self.stop_event = stop_event
        self.valores_obtenidos = []

    def analizar(self):
        try:
            while not self.stop_event.is_set():
                if self.conn.poll(0.5):  # evitar bloqueo, espera con timeout
                    try:
                        dato = self.conn.recv()
                    except EOFError:
                        print(f"[{self.tipo.upper()}] Pipe cerrado. Cerrando analizador.")
                        break

                    timestamp = dato["timestamp"]

                    if self.tipo != "presion":
                        valor = dato[self.tipo]
                    else:
                        valor = dato["presion"][0]

                    self.valores_obtenidos.append(valor)
                    if len(self.valores_obtenidos) > 30:
                        self.valores_obtenidos.pop(0)

                    valores_obtenidos_array = np.array(self.valores_obtenidos)
                    media = np.mean(valores_obtenidos_array)
                    desviacion = np.std(valores_obtenidos_array)

                    print(f"[{self.tipo.upper()}] Valores Obtenidos: {self.valores_obtenidos}")
                    print(f"[{self.tipo.upper()}] Valor: {valor} | Media: {media:.2f} | Desviación estándar: {desviacion:.2f}")

                    resultado = {
                        "tipo": self.tipo,
                        "timestamp": timestamp,
                        "media": media,
                        "desv": desviacion
                    }
                    self.verificador_queue.put(resultado)

            print(f"[{self.tipo.upper()}] Finalizando y enviando señal de cierre.")
            self.verificador_queue.put(None)  # señal para el verificador

        except KeyboardInterrupt:
            print(f"[{self.tipo.upper()}] Analizador interrumpido. Cerrando proceso.")
            self.verificador_queue.put(None)
        finally:
            self.conn.close()

def ejecutar_analizador(tipo, conn, verificador_queue, stop_event):
    analizador = Analizador(tipo, conn, verificador_queue, stop_event)
    analizador.analizar()
