"""Funciones puras de validación y normalización. Si el dato es inválido lanzan ErrorValidacion."""
import unicodedata

from logica import CANTIDAD_NOTAS, NOTA_MAX, NOTA_MIN

DNI_LONGITUD = 8


class ErrorValidacion(ValueError):
    """Dato inválido o regla incumplida. El mensaje se puede mostrar tal cual al usuario."""


class ErrorCursoDuplicado(ErrorValidacion):
    """Caso particular: el alumno ya tiene registrado ese curso (herencia de excepciones)."""


def normalizar_texto(texto):
    """Minúsculas, sin tildes y sin espacios repetidos (para comparar nombres y cursos)."""
    sin_tildes = "".join(
        c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn"
    )
    return " ".join(sin_tildes.lower().split())


def validar_texto_obligatorio(texto, campo):
    """Retorna el texto sin espacios repetidos; lanza ErrorValidacion si está vacío."""
    if texto is None or not texto.strip():
        raise ErrorValidacion(f"El campo '{campo}' no puede estar vacío.")
    return " ".join(texto.split())


def validar_dni(texto):
    """El DNI debe tener exactamente 8 dígitos numéricos. Retorna el DNI limpio."""
    dni = (texto or "").strip()
    if not (dni.isascii() and dni.isdigit() and len(dni) == DNI_LONGITUD):
        raise ErrorValidacion(f"El DNI debe tener exactamente {DNI_LONGITUD} dígitos numéricos.")
    return dni


def validar_notas(valores):
    """Convierte las notas (texto o enteros) y verifica cantidad y rango. Retorna una tupla de enteros."""
    try:
        notas = tuple(int(valor) for valor in valores)
    except (TypeError, ValueError):
        raise ErrorValidacion("Las notas deben ser números enteros.") from None
    if len(notas) != CANTIDAD_NOTAS:
        raise ErrorValidacion(f"Se requieren exactamente {CANTIDAD_NOTAS} notas.")
    if not all(NOTA_MIN <= nota <= NOTA_MAX for nota in notas):
        raise ErrorValidacion(f"Las notas deben estar entre {NOTA_MIN} y {NOTA_MAX}.")
    return notas
