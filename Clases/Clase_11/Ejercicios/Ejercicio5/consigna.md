## Ejercicio 5: Pipes anónimos entre padre e hijo

Cree un script en Python donde el proceso padre y el hijo se comuniquen usando un `os.pipe()`. El hijo deberá enviar un mensaje al padre, y este deberá imprimirlo por pantalla.

Debe usarse codificación binaria y control adecuado de cierre de descriptores.

---

## ✅ Verificación punto por punto:
- Codificación binaria: El mensaje se codifica con .encode('utf-8') y se transmite como bytes.
- Lectura binaria: El padre usa os.read(), que devuelve bytes.
- Decodificación para mostrarlo: Se usa .decode('utf-8') antes de imprimir.
- Cierre del descriptor de lectura (hijo): os.close(lector) en el hijo.
- Cierre del descriptor de escritura (padre): os.close(escritor) en el padre.
- Cierre de descriptores usados: Ambos procesos cierran lo que no usan y lo que sí, una vez terminado.

## Ejecutar
```bash
python3 ejercicio5.py
```