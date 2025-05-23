### Ejercicio 5: Chat Bidireccional

#Desarrolla un sistema de chat simple entre dos procesos usando pipes. Cada proceso debe poder enviar y 
# recibir mensajes simultáneamente, implementando una comunicación bidireccional completa.

# python3 5.chat_bidireccional.py
import os
import sys
import select
import signal
import threading

def setup_signal_handler():
    """Configura el manejador de señales para salir limpiamente con Ctrl+C"""
    def signal_handler(sig, frame):
        print("\nSaliendo del chat...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)

def read_messages(pipe, name, should_exit):
    """Función para leer mensajes del pipe en un hilo separado"""
    with os.fdopen(pipe, 'r') as reader:
        while not should_exit[0]:
            # Usar select para comprobar si hay datos para leer sin bloquear
            readable, _, _ = select.select([reader], [], [], 0.5)
            if readable:
                message = reader.readline().strip()
                if message:
                    print(f"\n{name}: {message}")
                    print("Tú > ", end='', flush=True)
                else:
                    # EOF - el otro extremo cerró el pipe
                    print(f"\n{name} ha dejado el chat.")
                    should_exit[0] = True
                    break

def chat_process(read_pipe, write_pipe, name, other_name):
    """Gestiona el proceso de chat para un participante"""
    try:
        # Inicializar objeto para controlar la salida del hilo
        should_exit = [False]
        
        # Configurar el manejador de señales
        setup_signal_handler()
        
        # Crear un hilo para leer mensajes del otro participante
        reader_thread = threading.Thread(
            target=read_messages, 
            args=(read_pipe, other_name, should_exit)
        )
        reader_thread.daemon = True  # El hilo terminará cuando el programa principal termine
        reader_thread.start()
        
        # Abrir el pipe de escritura
        with os.fdopen(write_pipe, 'w') as writer:
            print(f"¡Bienvenido al chat, {name}!")
            print(f"Estás chateando con {other_name}.")
            print("Escribe 'exit' para salir.\n")
            
            # Bucle principal para enviar mensajes
            while not should_exit[0]:
                message = input(f"Tú > ")
                
                if message.lower() == 'exit':
                    print("Saliendo del chat...")
                    should_exit[0] = True
                    break
                
                # Enviar el mensaje
                writer.write(f"{message}\n")
                writer.flush()
        
    except Exception as e:
        print(f"Error en el proceso de chat: {e}")
    finally:
        # Asegurarse de que los descriptores se cierren
        try:
            os.close(read_pipe)
            os.close(write_pipe)
        except:
            pass  # Ignorar errores al cerrar descriptores ya cerrados

def main():
    # Crear pipes para comunicación bidireccional
    pipe_a_to_b_r, pipe_a_to_b_w = os.pipe()  # A envía a B
    pipe_b_to_a_r, pipe_b_to_a_w = os.pipe()  # B envía a A
    
    # Bifurcar el proceso
    pid = os.fork()
    
    if pid > 0:  # Proceso padre (participante A)
        # Cerrar extremos no utilizados
        os.close(pipe_a_to_b_r)
        os.close(pipe_b_to_a_w)
        
        # Gestionar el chat como participante A
        chat_process(pipe_b_to_a_r, pipe_a_to_b_w, "Participante A", "Participante B")
        
        # Esperar a que el proceso hijo termine
        try:
            os.waitpid(pid, 0)
        except:
            pass
        
    else:  # Proceso hijo (participante B)
        # Cerrar extremos no utilizados
        os.close(pipe_a_to_b_w)
        os.close(pipe_b_to_a_r)
        
        # Gestionar el chat como participante B
        chat_process(pipe_a_to_b_r, pipe_b_to_a_w, "Participante B", "Participante A")
        
        # Salir del proceso hijo
        sys.exit(0)

if __name__ == "__main__":
    main()
    
    
"""
1. Implementamos un sistema de chat bidireccional completo entre dos procesos.
2. Utilizamos cuatro descriptores de archivo para crear dos pipes, uno para cada dirección de comunicación:
   - pipe_a_to_b para que A envíe mensajes a B
   - pipe_b_to_a para que B envíe mensajes a A
3. Cada proceso maneja el envío y recepción de mensajes simultáneamente:
   - Un hilo dedicado espera nuevos mensajes entrantes
   - El hilo principal se encarga de capturar la entrada del usuario y enviarla
4. Empleamos `select.select()` para verificar si hay datos disponibles para leer sin bloquear el hilo.
5. Implementamos un mecanismo para salir limpiamente del chat, tanto por comando del usuario como por señal (Ctrl+C).
6. Utilizamos manejo de excepciones para asegurar que los recursos se liberen correctamente en todos los casos.

Este ejercicio demuestra cómo implementar comunicación bidireccional completa entre procesos, incluyendo aspectos avanzados como la 
gestión de múltiples descriptores de archivo, hilos y señales.

"""