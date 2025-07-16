def verificador(conn):
    try:
        while True:
            try:
                resultado = conn.recv()
            except EOFError:
                print("[VERIFICADOR] Pipe cerrado. Cerrando verificador.")
                break  # Salir si el pipe se cerró

            print(f"[VERIFICADOR] Recibido: {resultado}")

    except KeyboardInterrupt:
        print("[VERIFICADOR] Interrumpido por el usuario. Cerrando proceso.")

    finally:
        conn.close()
