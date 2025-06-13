#!/bin/bash

echo "Listado de procesos activos:"
printf "%-6s | %-6s | %-25s | %s\n" "PID" "PPID" "Nombre" "Estado"
echo "---------------------------------------------------------------"

# Crear un array asociativo para contar estados
declare -A estados

# Recorrer los directorios numéricos en /proc (cada uno representa un proceso)
for pid in /proc/[0-9]*; do
    pid_num=$(basename "$pid")

    if [[ -r "$pid/status" ]]; then
        nombre=$(grep "^Name:" "$pid/status" | awk '{print $2}')
        ppid=$(grep "^PPid:" "$pid/status" | awk '{print $2}')
        estado=$(grep "^State:" "$pid/status" | awk '{print $2}')

        # Imprimir línea con formato fijo
        printf "%-6s | %-6s | %-25s | %s\n" "$pid_num" "$ppid" "$nombre" "$estado"

        ((estados["$estado"]++))
    fi
done

echo
echo "Resumen de estados:"
for estado in "${!estados[@]}"; do
    echo "Estado '$estado': ${estados[$estado]} proceso(s)"
done
