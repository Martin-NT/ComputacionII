import numpy as np

def analizador(tipo, conn, verificador_conn):
    valores_obtenidos = []
    try:
        while True:
            try:
                dato = conn.recv()
            except EOFError:
                print(f"[{tipo.upper()}] Pipe cerrado. Cerrando analizador.")
                break  # Salir si el pipe se cerró
            
            timestamp = dato["timestamp"]
            if tipo != "presion":
                valor = dato[tipo]
            else:
                valor = dato["presion"][0]  # presión sistólica

            valores_obtenidos.append(valor)
            if len(valores_obtenidos) > 30:
                valores_obtenidos.pop(0)

            valores_obtenidos_array = np.array(valores_obtenidos)
            media = np.mean(valores_obtenidos_array)
            desviacion = np.std(valores_obtenidos_array)
            
            print(f"[{tipo.upper()}] Valores Obtenidos: {valores_obtenidos}")
            print(f"[{tipo.upper()}] Valor: {valor} | Media: {media:.2f} | Desviación estándar: {desviacion:.2f}")

            resultado = {
                "tipo": tipo,
                "timestamp": timestamp,
                "media": media,
                "desv": desviacion
            }
            verificador_conn.send(resultado)

    except KeyboardInterrupt:
        print(f"[{tipo.upper()}] Analizador interrumpido. Cerrando proceso.")

    finally:
        conn.close()
        verificador_conn.close()
