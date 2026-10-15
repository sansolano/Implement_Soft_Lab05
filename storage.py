import json
import os
from datetime import datetime

CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
ARCHIVO = os.path.join(CARPETA, "historial_validaciones.json")


def cargar_historial():
    """Lee el historial. Si no existe o esta danado, devuelve una lista vacia."""
    if not os.path.exists(ARCHIVO):
        return []
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(datos, list):
        return []
    return datos


def guardar_historial(registros):
    os.makedirs(os.path.dirname(ARCHIVO), exist_ok=True)
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(registros, archivo, ensure_ascii=False, indent=2)


def agregar_registro(entrada, resultado):
    """Agrega una validacion al historial y devuelve el registro creado."""
    registro = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "valor": str(entrada)[:30],
        "resultado": "Aceptado" if resultado["valido"] else "Rechazado",
        "motivo": "" if resultado["valido"] else resultado["mensaje"],
    }
    registros = cargar_historial()
    registros.append(registro)
    guardar_historial(registros)
    return registro


def borrar_historial():
    guardar_historial([])
