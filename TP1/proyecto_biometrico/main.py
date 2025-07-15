import multiprocessing
import time
import datetime
import random
import signal
import os

def generar_dato():
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "frecuencia": random.randint(60, 180),
        "presion": [random.randint(110, 180), random.randint(70, 110)],
        "oxigeno": random.randint(90, 100)
    }

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

        print(f"[{tipo.upper()}] Recibido: {valor}")


def main():
    # Crear pipes
    padre_a, hijo_a = multiprocessing.Pipe()
    padre_b, hijo_b = multiprocessing.Pipe()
    padre_c, hijo_c = multiprocessing.Pipe()

    # Crear procesos
    proceso_a = multiprocessing.Process(target=analizador, args=("frecuencia", hijo_a))
    proceso_b = multiprocessing.Process(target=analizador, args=("presion", hijo_b))
    proceso_c = multiprocessing.Process(target=analizador, args=("oxigeno", hijo_c))

    # Iniciar procesos
    proceso_a.start()
    proceso_b.start()
    proceso_c.start()

    try:
        for _ in range(60):  # 60 segundos de prueba de esfuerzo
            dato = generar_dato()
            padre_a.send(dato)
            padre_b.send(dato)
            padre_c.send(dato)
            print(f"[MAIN] Enviado dato: {dato}")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
        
    finally:
        padre_a.close()
        padre_b.close()
        padre_c.close()

        proceso_a.join()
        proceso_b.join()
        proceso_c.join()

if __name__ == "__main__":
    main()
