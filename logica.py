"""Reglas de negocio puras (sin interfaz, sin archivos): constantes, promedio y estado."""

CANTIDAD_NOTAS = 4
NOTA_MIN = 0
NOTA_MAX = 20
NOTA_APROBATORIA = 11

APROBADO = "APROBADO"
DESAPROBADO = "DESAPROBADO"
INVALIDO = "INVÁLIDO"


def calcular_promedio(notas):
    return sum(notas) / len(notas)


def determinar_estado(promedio):
    """DESAPROBADO por debajo de 11, APROBADO hasta 20 e INVÁLIDO si se pasa de 20."""
    if promedio < NOTA_APROBATORIA:
        return DESAPROBADO
    if promedio <= NOTA_MAX:
        return APROBADO
    return INVALIDO
