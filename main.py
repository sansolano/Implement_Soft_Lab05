import webbrowser

from server import crear_servidor

PUERTO = 8000

if __name__ == "__main__":
    servidor = crear_servidor(PUERTO)
    url = f"http://127.0.0.1:{PUERTO}"
    webbrowser.open(url)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.server_close()
