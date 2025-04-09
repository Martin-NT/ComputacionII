### Ejercicio 2: Contador de Palabras

# Implementa un sistema donde el proceso padre lee un archivo de texto y envía su contenido línea por línea 
# a un proceso hijo a través de un pipe. El hijo debe contar las palabras en cada línea y devolver el resultado al padre.

#python3 2.contador_de_palabras.py
import os
import sys

def main():
    # Crear pipes para la comunicación
    content_pipe_r, content_pipe_w = os.pipe()  # Para enviar contenido del archivo
    count_pipe_r, count_pipe_w = os.pipe()      # Para enviar conteos de palabras
    
    # Bifurcar el proceso
    pid = os.fork()
    
    if pid > 0:  # Proceso padre
        # Cerrar extremos no utilizados
        os.close(content_pipe_r)
        os.close(count_pipe_w)
        
        # Nombre del archivo a procesar
        filename = "sample_text.txt"
        
        try:
            # Si el archivo no existe, creamos uno de ejemplo
            if not os.path.exists(filename):
                with open(filename, 'w') as f:
                    f.write("Este es un archivo de ejemplo.\n")
                    f.write("Contiene algunas líneas de texto.\n")
                    f.write("Para demostrar el contador de palabras.\n")
                    f.write("Usando pipes en Python.")
            
            # Abrir y leer el archivo
            with open(filename, 'r') as file:
                print(f"Padre: Leyendo archivo '{filename}'")
                
                # Convertir el descriptor a un objeto de archivo para escritura
                pipe_writer = os.fdopen(content_pipe_w, 'w')
                
                # Enviar cada línea al hijo
                line_count = 0
                for line in file:
                    pipe_writer.write(line)
                    pipe_writer.flush()  # Importante para asegurar que los datos se envíen
                    line_count += 1
                
                print(f"Padre: Enviadas {line_count} líneas al hijo")
                pipe_writer.close()  # Esto cierra content_pipe_w
                
                # Leer resultados del hijo
                pipe_reader = os.fdopen(count_pipe_r, 'r')
                
                # Imprimir los conteos recibidos
                print("\nConteo de palabras por línea:")
                total_words = 0
                for i, count in enumerate(pipe_reader, 1):
                    count = int(count.strip())
                    total_words += count
                    print(f"Línea {i}: {count} palabras")
                
                print(f"\nTotal de palabras: {total_words}")
                pipe_reader.close()  # Esto cierra count_pipe_r
        
        except Exception as e:
            print(f"Error en el padre: {e}")
            # Cerrar los pipes en caso de error
            os.close(content_pipe_w)
            os.close(count_pipe_r)
        
        # Esperar a que el hijo termine
        os.waitpid(pid, 0)
        
    else:  # Proceso hijo
        try:
            # Cerrar extremos no utilizados
            os.close(content_pipe_w)
            os.close(count_pipe_r)
            
            # Convertir descriptores a objetos de archivo
            content_reader = os.fdopen(content_pipe_r, 'r')
            count_writer = os.fdopen(count_pipe_w, 'w')
            
            print("Hijo: Esperando líneas para contar palabras...")
            
            # Procesar cada línea recibida
            for line in content_reader:
                # Contar palabras (dividir por espacios)
                word_count = len(line.split())
                
                # Enviar conteo al padre
                count_writer.write(f"{word_count}\n")
                count_writer.flush()  # Asegurar que los datos se envíen
            
            # Cerrar los pipes
            content_reader.close()
            count_writer.close()
            
        except Exception as e:
            print(f"Error en el hijo: {e}")
            # Cerrar los pipes en caso de error
            os.close(content_pipe_r)
            os.close(count_pipe_w)
        
        # Salir del proceso hijo
        sys.exit(0)

if __name__ == "__main__":
    main()
    
#**Explicación:**
#1. Creamos dos pipes: uno para enviar el contenido del archivo del padre al hijo y otro para que el hijo devuelva los conteos al padre.
#2. El padre lee un archivo línea por línea y envía cada línea al hijo a través del primer pipe.
#3. El hijo lee cada línea, cuenta las palabras dividiendo por espacios y envía el conteo al padre a través del segundo pipe.
#4. Utilizamos objetos de archivo Python (`os.fdopen()`) para una manipulación más conveniente de los pipes.
#5. Implementamos manejo de errores para asegurar que los recursos se liberen correctamente en caso de problemas.
#6. Si el archivo de ejemplo no existe, lo creamos automáticamente para facilitar la prueba.

#Este ejercicio demuestra un patrón común en el procesamiento de datos con pipes: un proceso envía datos para ser procesados, 
# y otro realiza el procesamiento y devuelve resultados.

"""
Padre: Leyendo archivo 'sample_text.txt'
Padre: Enviadas 4 líneas al hijo

Conteo de palabras por línea:
Hijo: Esperando líneas para contar palabras...
Línea 1: 6 palabras
Línea 2: 5 palabras
Línea 3: 6 palabras
Línea 4: 4 palabras

Total de palabras: 21

"""