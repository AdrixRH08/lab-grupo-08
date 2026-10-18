def validar_texto_obligatorio(texto):
    return texto is not None and texto.strip() != ""


def validar_nota(nota):
    return 0 <= nota <= 20


def validar_dni(dni):
    """El DNI debe tener exactamente 8 dígitos numéricos."""
    return dni.isascii() and dni.isdigit() and len(dni) == 8


def convertir_notas(textos):
    """Convierte la lista de textos a enteros. Retorna None si alguno no es entero."""
    try:
        return [int(texto) for texto in textos]
    except ValueError:
        return None


def curso_ya_registrado(lista, dni, curso, ignorar=None):
    """True si ese alumno ya tiene registrado ese curso (se puede ignorar un índice al editar)."""
    for i, registro in enumerate(lista):
        if i == ignorar:
            continue
        if registro["dni"] == dni and registro["curso"].strip().lower() == curso.strip().lower():
            return True
    return False


def nombre_coincide(lista, dni, nombre):
    """True si el DNI es nuevo o si ya está registrado con ese mismo nombre."""
    for registro in lista:
        if registro["dni"] == dni:
            return registro["user"].strip().lower() == nombre.strip().lower()
    return True