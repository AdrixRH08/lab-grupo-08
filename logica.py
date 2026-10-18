def calcular_promedio(n1, n2, n3, n4):
    return (n1 + n2 + n3 + n4) / 4


def determinar_estado(promedio):
    if promedio < 11:
        return "DESAPROBADO"
    elif promedio <= 20:
        return "APROBADO"
    else:
        return "INVÁLIDO"


def crear_registro(dni, user, curso, notas):
    """Arma el registro (alumno + curso) con su promedio y estado ya calculados."""
    promedio = calcular_promedio(notas[0], notas[1], notas[2], notas[3])
    return {
        "dni": dni,
        "user": user,
        "curso": curso,
        "notas": notas,
        "promedio": promedio,
        "estado": determinar_estado(promedio),
    }