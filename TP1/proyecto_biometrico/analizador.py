import numpy as np

class Analizador:
    def __init__(self, tipo, conn, verificador_conn):
        self.tipo = tipo
        self.conn = conn
        self.verificador_conn = verificador_conn
        self.valores_obtenidos = []

    def analizar(self):
        try:
            while True:
                try:
                    dato = self.conn.recv()
                except EOFError:
                    print(f"[{self.tipo.upper()}] Pipe cerrado. Cerrando analizador.")
                    break

                timestamp = dato["timestamp"]

                if self.tipo != "presion":
                    valor = dato[self.tipo]
                else:
                    valor = dato["presion"][0]  # presión sistólica

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
                self.verificador_conn.send(resultado)

        except KeyboardInterrupt:
            print(f"[{self.tipo.upper()}] Analizador interrumpido. Cerrando proceso.")
        finally:
            self.conn.close()
            self.verificador_conn.close()

def ejecutar_analizador(tipo, conn, verificador_conn):
    analizador = Analizador(tipo, conn, verificador_conn)
    analizador.analizar()