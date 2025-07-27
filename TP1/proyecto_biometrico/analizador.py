import numpy as np

class Analizador:
    def __init__(self, tipo, conn, verificador_queue, stop_event, semaphore):
        self.tipo = tipo
        self.conn = conn
        self.verificador_queue = verificador_queue
        self.stop_event = stop_event
        self.semaphore = semaphore
        self.valores_obtenidos = []

    def analizar(self):
        try:
            while not self.stop_event.is_set():
                if self.conn.poll(0.5):  # evita bloqueo
                    try:
                        dato = self.conn.recv()
                    except EOFError:
                        print(f"[{self.tipo.upper()}] ❌ Pipe cerrado. Cerrando analizador.")
                        break

                    if dato is None:
                        print(f"[{self.tipo.upper()}] ✅ Señal de fin recibida.")
                        break  # fin de datos

                    timestamp = dato["timestamp"]

                    if self.tipo != "presion":
                        valor = dato[self.tipo]
                    else:
                        valor = dato["presion"][0]

                    self.valores_obtenidos.append(valor)
                    if len(self.valores_obtenidos) > 30:
                        self.valores_obtenidos.pop(0)

                    media = np.mean(self.valores_obtenidos)
                    desviacion = np.std(self.valores_obtenidos)

                    resultado = {
                        "tipo": self.tipo,
                        "timestamp": timestamp,
                        "media": media,
                        "desv": desviacion,
                        "ventana": list(self.valores_obtenidos)
                    }

                    with self.semaphore:
                        self.verificador_queue.put(resultado)

            print(f"[{self.tipo.upper()}] ⛔ Finalizando y enviando señal de cierre.")
            self.verificador_queue.put(None)

        except KeyboardInterrupt:
            print(f"[{self.tipo.upper()}] ⛔ Interrumpido por el usuario.")
            self.verificador_queue.put(None)

        finally:
            self.conn.close()

def ejecutar_analizador(tipo, conn, verificador_queue, stop_event, semaphore):
    analizador = Analizador(tipo, conn, verificador_queue, stop_event, semaphore)
    analizador.analizar()
