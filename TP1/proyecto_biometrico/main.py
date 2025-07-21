import multiprocessing
import time
from generador import GeneradorBiometrico
from analizador import ejecutar_analizador
from verificador import Verificador

def main():
    generador = GeneradorBiometrico()

    
    padre_a, hijo_a = multiprocessing.Pipe()
    padre_b, hijo_b = multiprocessing.Pipe()
    padre_c, hijo_c = multiprocessing.Pipe()

    verificador_padre, verificador_hijo = multiprocessing.Pipe()

    proceso_a = multiprocessing.Process(target = ejecutar_analizador, args=("frecuencia", hijo_a, verificador_padre))
    proceso_b = multiprocessing.Process(target = ejecutar_analizador, args=("presion", hijo_b, verificador_padre))
    proceso_c = multiprocessing.Process(target = ejecutar_analizador, args=("oxigeno", hijo_c, verificador_padre))

    proceso_verificador = multiprocessing.Process(target=Verificador(verificador_hijo).verificar)

    proceso_a.start()
    proceso_b.start()
    proceso_c.start()
    proceso_verificador.start()

    hijo_a.close()
    hijo_b.close()
    hijo_c.close()
    verificador_hijo.close()

    try:
        for _ in range(60):
            dato = generador.generar_dato()
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
        verificador_padre.close()

        proceso_a.join()
        proceso_b.join()
        proceso_c.join()
        proceso_verificador.join()

if __name__ == "__main__":
    main()
