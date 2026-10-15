MINIMO = 1
MAXIMO = 100
DIGITOS = "0123456789"


def solo_digitos(texto):
    if texto == "":
        return False
    for caracter in texto:
        if caracter not in DIGITOS:
            return False
    return True


def validar_cantidad(entrada):
    if entrada is None:
        entrada = ""
    texto = str(entrada).strip()  # se ignoran espacios al inicio y al final

    # 1. Campo vacio
    if texto == "":
        return rechazar("El campo está vacío. Ingrese una cantidad entre 1 y 100.")

    # 2. Numero negativo (ej: -5)
    if texto.startswith("-") and solo_digitos(texto[1:]):
        return rechazar("La cantidad debe ser mayor o igual a 1.")

    # 3. Numero entero: se revisa el rango
    if solo_digitos(texto):
        if len(texto) > 10:  # evita convertir numeros gigantes
            return rechazar("La cantidad no puede ser mayor a 100.")
        numero = int(texto)
        if numero < MINIMO:
            return rechazar("La cantidad debe ser mayor o igual a 1.")
        if numero > MAXIMO:
            return rechazar("La cantidad no puede ser mayor a 100.")
        return {"valido": True, "mensaje": "Cantidad válida.", "valor": numero}

    # 4. Numero decimal (ej: 5.5 o 5,5)
    sin_separador = texto.lstrip("-").replace(".", "", 1).replace(",", "", 1)
    if solo_digitos(sin_separador):
        return rechazar("No se permiten números decimales.")

    # 5. Cualquier otra cosa: letras, simbolos o mezcla
    tiene_letras = any(c.isalpha() for c in texto)
    tiene_numeros = any(c in DIGITOS for c in texto)
    if tiene_letras and tiene_numeros:
        return rechazar("No se permite mezclar números y letras.")
    if tiene_letras:
        return rechazar("No se permiten letras.")
    return rechazar("No se permiten símbolos ni espacios.")


def rechazar(mensaje):
    return {"valido": False, "mensaje": mensaje, "valor": None}
