import multiprocessing
import time
from generador import generar_dato
from analizador import analizador

def main():
    padre_a, hijo_a = multiprocessing.Pipe()
    padre_b, hijo_b = multiprocessing.Pipe()
    padre_c, hijo_c = multiprocessing.Pipe()

    proceso_a = multiprocessing.Process(target=analizador, args=("frecuencia", hijo_a))
    proceso_b = multiprocessing.Process(target=analizador, args=("presion", hijo_b))
    proceso_c = multiprocessing.Process(target=analizador, args=("oxigeno", hijo_c))

    proceso_a.start()
    proceso_b.start()
    proceso_c.start()

    try:
        for _ in range(60):
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
