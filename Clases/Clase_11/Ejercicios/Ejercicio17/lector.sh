#!/bin/bash
while true; do
    if read linea < /tmp/mi_fifo; then
        echo "Lector recibió: $linea"
    fi
done
