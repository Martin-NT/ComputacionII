import numpy as np 

def analizador(tipo, conn):
    ventana = []
    while True:
        try:
            dato = conn.recv()
        except EOFError:
            break  # El pipe fue cerrado

        if tipo != "presion":
            valor = dato[tipo]
        else:
            valor = dato["presion"][0]  # presión sistólica

        ventana.append(valor)
        if len(ventana) > 30:
            ventana.pop(0)
            
        ventana_array = np.array(ventana)
        media = np.mean(ventana_array)
        desviacion = np.std(ventana_array)

        print(f"[{tipo.upper()}] Valor: {valor} | Media: {media:.2f} | Desviación estándar: {desviacion:.2f}")
