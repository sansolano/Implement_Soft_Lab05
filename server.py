import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

import storage
from validator import validar_cantidad

CARPETA_WEB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


ARCHIVOS = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/styles.css": ("styles.css", "text/css; charset=utf-8"),
    "/app.js": ("app.js", "application/javascript; charset=utf-8"),
}


class Manejador(BaseHTTPRequestHandler):

    def enviar(self, codigo, contenido, tipo):
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)

    def enviar_json(self, datos, codigo=200):
        contenido = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.enviar(codigo, contenido, "application/json; charset=utf-8")

    def do_GET(self):
        if self.path == "/api/historial":
            registros = storage.cargar_historial()
            registros.reverse()  # el mas reciente primero
            self.enviar_json(registros)
        elif self.path in ARCHIVOS:
            nombre, tipo = ARCHIVOS[self.path]
            with open(os.path.join(CARPETA_WEB, nombre), "rb") as archivo:
                self.enviar(200, archivo.read(), tipo)
        else:
            self.enviar_json({"error": "No encontrado"}, 404)

    def do_POST(self):
        if self.path != "/api/validar":
            self.enviar_json({"error": "No encontrado"}, 404)
            return
        try:
            largo = int(self.headers.get("Content-Length", 0))
            if largo > 1000:
                raise ValueError("Peticion muy grande")
            datos = json.loads(self.rfile.read(largo) or b"{}")
            entrada = datos.get("cantidad", "")
        except (ValueError, AttributeError):
            self.enviar_json({"error": "Peticion invalida"}, 400)
            return

        resultado = validar_cantidad(entrada)
        storage.agregar_registro(entrada, resultado)
        self.enviar_json(resultado)

    def do_DELETE(self):
        if self.path == "/api/historial":
            storage.borrar_historial()
            self.enviar_json({"ok": True})
        else:
            self.enviar_json({"error": "No encontrado"}, 404)

    def log_message(self, formato, *args):
        pass


def crear_servidor(puerto=8000):
    return HTTPServer(("127.0.0.1", puerto), Manejador)
