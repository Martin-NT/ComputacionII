import multiprocessing
import time
from generador import GeneradorBiometrico
from analizador import ejecutar_analizador
from verificador import Verificador

def main():
    generador = GeneradorBiometrico()

    # Pipes para enviar datos del generador a cada analizador
    padre_a, hijo_a = multiprocessing.Pipe()
    padre_b, hijo_b = multiprocessing.Pipe()
    padre_c, hijo_c = multiprocessing.Pipe()

    # Colas para enviar resultados de analizadores al verificador
    queue_a = multiprocessing.Queue()
    queue_b = multiprocessing.Queue()
    queue_c = multiprocessing.Queue()

    stop_event = multiprocessing.Event()
    lock = multiprocessing.Lock()
    semaphore = multiprocessing.Semaphore(2)  # Máximo 2 analizadores al mismo tiempo

    # Crear procesos analizadores
    proceso_a = multiprocessing.Process(target=ejecutar_analizador, args=("frecuencia", hijo_a, queue_a, stop_event, semaphore))
    proceso_b = multiprocessing.Process(target=ejecutar_analizador, args=("presion", hijo_b, queue_b, stop_event, semaphore))
    proceso_c = multiprocessing.Process(target=ejecutar_analizador, args=("oxigeno", hijo_c, queue_c, stop_event, semaphore))

    # Crear proceso verificador
    proceso_verificador = multiprocessing.Process(
        target=Verificador([queue_a, queue_b, queue_c], stop_event, lock).verificar
    )

    # Iniciar procesos
    proceso_a.start()
    proceso_b.start()
    proceso_c.start()
    proceso_verificador.start()

    # Cerrar extremos no usados del pipe
    hijo_a.close()
    hijo_b.close()
    hijo_c.close()

    try:
        for _ in range(60):
            dato = generador.generar_dato()
            padre_a.send(dato)
            padre_b.send(dato)
            padre_c.send(dato)
            print(f"[MAIN] 📤 Enviado dato: {dato}")
            time.sleep(1)

    except KeyboardInterrupt:
        print("--> ⛔ Interrumpido por el usuario.")
    
    finally:
        print("[MAIN] 🧹 Enviando señales de finalización...")

        # Señal explícita de finalización a los analizadores
        padre_a.send(None)
        padre_b.send(None)
        padre_c.send(None)

        # Cerrar los extremos de los pipes
        padre_a.close()
        padre_b.close()
        padre_c.close()

        # Setea el evento de detención para el verificador
        stop_event.set()

        # Esperar que terminen todos
        proceso_a.join()
        proceso_b.join()
        proceso_c.join()
        proceso_verificador.join()

        print("[MAIN] ✅ Todos los procesos finalizaron correctamente.")

if __name__ == "__main__":
    main()
