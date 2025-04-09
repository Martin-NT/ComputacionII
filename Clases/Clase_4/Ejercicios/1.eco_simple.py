
""" Ejercicio 1: Eco Simple """

# Crea un programa en Python que establezca comunicación entre un proceso padre y un hijo mediante un pipe. 
# El padre debe enviar un mensaje al hijo, y el hijo debe recibir ese mensaje y devolverlo al padre (eco).

# Ejecutar en la terminal con el comando: python3 1.eco_simple.py

import os
import sys

def main():
    # Crear dos pipes: uno para enviar del padre al hijo, otro para recibir respuesta
    parent_to_child_r, parent_to_child_w = os.pipe() #se usa para que el padre le escriba al hijo
    child_to_parent_r, child_to_parent_w = os.pipe() #se usa para que el hijo le escriba al padre
    
    # Bifurcar el proceso
    pid = os.fork()
    # Si pid > 0, estamos en el padre.
    # Si pid == 0, estamos en el hijo.
    
    if pid > 0:  # Proceso padre
        # Cerrar extremos no utilizados
        os.close(parent_to_child_r)
        os.close(child_to_parent_w)
        
        # Mensaje a enviar
        message = "Hola, proceso hijo!"
        print(f"Padre: Enviando mensaje: '{message}'")
        
        # Enviar mensaje al hijo
        os.write(parent_to_child_w, message.encode())
        os.close(parent_to_child_w)  # Cerrar después de escribir
        
        # Recibir respuesta del hijo
        response = os.read(child_to_parent_r, 1024).decode()
        os.close(child_to_parent_r)  # Cerrar después de leer
        
        print(f"Padre: Recibí respuesta: '{response}'")
        
        # Esperar a que el hijo termine
        os.waitpid(pid, 0)
        
    else:  # Proceso hijo
        # Cerrar extremos no utilizados
        os.close(parent_to_child_w)
        os.close(child_to_parent_r)
        
        # Leer mensaje del padre
        message = os.read(parent_to_child_r, 1024).decode()
        os.close(parent_to_child_r)  # Cerrar después de leer
        
        print(f"Hijo: Recibí mensaje: '{message}'")
        
        # Enviar eco al padre
        os.write(child_to_parent_w, message.encode())
        os.close(child_to_parent_w)  # Cerrar después de escribir
        
        # Salir del proceso hijo
        sys.exit(0)

if __name__ == "__main__":
    main()
    
    
# 💡 Tips y buenas prácticas
 
# Cerrar los extremos no usados evita bloqueos y permite recibir EOF correctamente.
# Siempre codificás los mensajes con .encode() y los decodificás con .decode(), porque os.read() y 
# os.write() trabajan con bytes.
# Este ejemplo es fundamental para entender cómo funcionan los pipes y fork() a nivel bajo en UNIX/Linux.

# **Explicación:**

# 1. Creamos dos pipes para comunicación bidireccional: uno para que el padre envíe mensajes al hijo y 
# otro para que el hijo responda al padre.

# 2. Después de bifurcar el proceso con `os.fork()`, asignamos roles diferentes al padre y al hijo.

# 3. Cerramos cuidadosamente los extremos de los pipes que cada proceso no utilizará, lo que es una 
# buena práctica para evitar deadlocks.

# 4. El padre envía un mensaje, el hijo lo lee y envía el mismo mensaje de vuelta como eco.

# 5. Cada proceso cierra sus descriptores de archivo después de usarlos.

# 6. El padre espera a que el hijo termine antes de finalizar.

#Este ejercicio ilustra los conceptos básicos de comunicación bidireccional usando pipes y la correcta gestión de descriptores de archivo.