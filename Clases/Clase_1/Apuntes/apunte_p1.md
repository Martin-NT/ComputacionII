# Resumen de la Clase de Computación II

## 1. **Configuración de Git**
   - **¿Qué es Git?**  
     Git es un sistema de control de versiones distribuido que permite gestionar y realizar seguimientos de los cambios en proyectos de software.
   - **¿Por qué es importante?**  
     Git facilita la colaboración en equipo y la gestión de versiones de un proyecto, asegurando que cada cambio quede registrado y se pueda revertir si es necesario.
   - **Instalación de Git**  
     Instalamos Git en nuestro sistema operativo y configuramos nuestra identidad con los comandos:
     ```bash
     git config --global user.name "Tu Nombre"
     git config --global user.email "tu.email@example.com"
     ```

## 2. **Creación de tu primer repositorio**
   - **Inicialización del repositorio local**  
     Creamos un repositorio local en Git y verificamos el estado con `git status`.
   - **Primer commit**  
     Realizamos un primer commit con el comando `git commit -m "mensaje del commit"`.
   - **Verificación del historial de commits**  
     Usamos `git log --oneline` para ver el historial de commits.

## 3. **Conexión con un repositorio remoto en GitHub**
   - **Creación de un repositorio en GitHub**  
     Creamos un repositorio vacío en GitHub.
   - **Conexión del repositorio local con GitHub**  
     Usamos el comando `git remote add origin <url_del_repositorio>`.
   - **Subir cambios al repositorio remoto**  
     Subimos los commits locales a GitHub con `git push -u origin master`.

## 4. **Estructura del repositorio**
   - Creamos la siguiente estructura de directorios para organizar nuestro proyecto:
     ```
     README.md
     /TP_1
     /TP_2
     /Clases
         /Clase_1
             /Apuntes
             /Ejercicios
             /Resumen_pedagógico
         /Clase_2
             /Apuntes
             /Ejercicios
             /Resumen_pedagógico
         ...
     /TRABAJO_FINAL
     ```
   - **Creación de carpetas y archivos** con los comandos `mkdir` para las clases y los trabajos prácticos.

## 5. **Conceptos básicos de la terminal Unix/Linux**
   - **Entrada/Salida estándar (stdin, stdout, stderr)**  
     Explicamos los tres flujos principales en Unix/Linux.
   - **Redirección de salida e entrada**
     - `>`: Redirigir la salida estándar a un archivo.
     - `>>`: Agregar la salida estándar a un archivo.
     - `<`: Redirigir la entrada estándar desde un archivo.
     - `2>`: Redirigir los errores estándar a un archivo.
   - **Uso de pipes (`|`)**  
     Encadenamos comandos con pipes para pasar la salida de uno como entrada del siguiente.
   - **Archivos especiales como `/dev/null`**  
     Utilizamos `/dev/null` para descartar salidas no deseadas.

## 6. **Práctica y verificación**
   - **Ejercicios prácticos** para redirigir la salida, filtrar resultados con pipes y manejar errores estándar.
   - Verificamos que todo estuviera correcto mediante `git status`, `git log`, y la comprobación en GitHub.

---

## **Próximos pasos**
   - **Verificar con el profesor y compañeros** que todo esté bien organizado.
   - **Seguir practicando** con Git y la terminal para mejorar tus habilidades.

