### Ejercicio 3: Pipeline de Filtrado

#Crea una cadena de tres procesos conectados por pipes donde: el primer proceso genera números aleatorios entre 1 y 100, 
# el segundo proceso filtra solo los números pares, y el tercer proceso calcula el cuadrado de estos números pares.

# python3 3.pipeline_de_filtrado.py
import os
import sys
import random
import time

def generator_process(write_pipe):
    """Genera números aleatorios entre 1 y 100."""
    try:
        with os.fdopen(write_pipe, 'w') as pipe:
            print("Generador: Produciendo 10 números aleatorios...")
            for _ in range(10):
                num = random.randint(1, 100)
                pipe.write(f"{num}\n")
                pipe.flush()
                print(f"Generador: Generé el número {num}")
                time.sleep(0.5)  # Pequeña pausa para mejor visualización
    except Exception as e:
        print(f"Error en generador: {e}")
    finally:
        print("Generador: Terminando...")

def filter_process(read_pipe, write_pipe):
    """Filtra solo los números pares."""
    try:
        with os.fdopen(read_pipe, 'r') as in_pipe, os.fdopen(write_pipe, 'w') as out_pipe:
            print("Filtro: Filtrando números pares...")
            for line in in_pipe:
                num = int(line.strip())
                if num % 2 == 0:  # Solo procesar números pares
                    out_pipe.write(f"{num}\n")
                    out_pipe.flush()
                    print(f"Filtro: Pasando número par {num}")
                else:
                    print(f"Filtro: Descartando número impar {num}")
                time.sleep(0.3)  # Pequeña pausa
    except Exception as e:
        print(f"Error en filtro: {e}")
    finally:
        print("Filtro: Terminando...")

def square_process(read_pipe):
    """Calcula el cuadrado de los números recibidos."""
    try:
        with os.fdopen(read_pipe, 'r') as pipe:
            print("Cuadrador: Calculando cuadrados...")
            results = []
            for line in pipe:
                num = int(line.strip())
                square = num * num
                results.append((num, square))
                print(f"Cuadrador: {num}² = {square}")
                time.sleep(0.3)  # Pequeña pausa
            
            # Mostrar resumen final
            print("\nResultados finales:")
            for num, square in results:
                print(f"{num}² = {square}")
            print(f"Total de números procesados: {len(results)}")
    except Exception as e:
        print(f"Error en cuadrador: {e}")
    finally:
        print("Cuadrador: Terminando...")

def main():
    # Crear pipes para conectar los procesos
    pipe1_r, pipe1_w = os.pipe()  # Conecta generador -> filtro
    pipe2_r, pipe2_w = os.pipe()  # Conecta filtro -> cuadrador
    
    # Crear el primer proceso hijo (generador)
    pid1 = os.fork()
    
    if pid1 == 0:  # Proceso generador
        # Cerrar pipes no utilizados
        os.close(pipe1_r)
        os.close(pipe2_r)
        os.close(pipe2_w)
        
        # Ejecutar la función generadora
        generator_process(pipe1_w)
        sys.exit(0)
    
    # Crear el segundo proceso hijo (filtro)
    pid2 = os.fork()
    
    if pid2 == 0:  # Proceso filtro
        # Cerrar pipes no utilizados
        os.close(pipe1_w)
        os.close(pipe2_r)
        
        # Ejecutar la función de filtrado
        filter_process(pipe1_r, pipe2_w)
        sys.exit(0)
    
    # Proceso principal (cuadrador)
    # Cerrar pipes no utilizados
    os.close(pipe1_r)
    os.close(pipe1_w)
    os.close(pipe2_w)
    
    # Ejecutar la función cuadradora
    square_process(pipe2_r)
    
    # Esperar a que los procesos hijos terminen
    os.waitpid(pid1, 0)
    os.waitpid(pid2, 0)
    
    print("Pipeline completado.")

if __name__ == "__main__":
    main()
    
"""**Explicación:**
1. Implementamos tres procesos conectados mediante dos pipes, formando un pipeline de procesamiento:
   - El proceso generador produce números aleatorios.
   - El proceso filtro recibe estos números y solo deja pasar los pares.
   - El proceso cuadrador calcula el cuadrado de los números pares recibidos.
2. Cada proceso tiene su propia función dedicada con manejo de excepciones.
3. Usamos pequeñas pausas (sleep) para facilitar la visualización del flujo de datos.
4. Incluimos mensajes de depuración para mostrar cada paso del procesamiento.
5. El proceso principal (padre) cierra adecuadamente los descriptores que no utiliza y espera a que ambos hijos terminen.

Este ejercicio ilustra el poderoso patrón de pipeline, donde los datos fluyen a través de múltiples etapas de procesamiento, 
cada una realizando una transformación específica.
"""

"""
Cuadrador: Calculando cuadrados...
Generador: Produciendo 10 números aleatorios...
Filtro: Filtrando números pares...
Generador: Generé el número 40
Filtro: Pasando número par 40
Cuadrador: 40² = 1600
Generador: Generé el número 36
Filtro: Pasando número par 36
Cuadrador: 36² = 1296
Generador: Generé el número 6
Filtro: Pasando número par 6
Cuadrador: 6² = 36
Generador: Generé el número 34
Filtro: Pasando número par 34
Cuadrador: 34² = 1156
Generador: Generé el número 54
Filtro: Pasando número par 54
Cuadrador: 54² = 2916
Generador: Generé el número 100
Filtro: Pasando número par 100
Cuadrador: 100² = 10000
Generador: Generé el número 48
Filtro: Pasando número par 48
Cuadrador: 48² = 2304
Generador: Generé el número 33
Filtro: Descartando número impar 33
Generador: Generé el número 50
Filtro: Pasando número par 50
Cuadrador: 50² = 2500
Generador: Generé el número 93
Filtro: Descartando número impar 93
Generador: Terminando...

Resultados finales:Filtro: Terminando...

40² = 1600
36² = 1296
6² = 36
34² = 1156
54² = 2916
100² = 10000
48² = 2304
50² = 2500
Total de números procesados: 8
Cuadrador: Terminando...
Pipeline completado.

"""