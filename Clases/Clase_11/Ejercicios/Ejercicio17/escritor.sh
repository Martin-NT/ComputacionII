#!/bin/bash
contador=0
while true; do
    echo "Mensaje $contador desde el escritor" > /tmp/mi_fifo
    ((contador++))
    sleep 1
done
