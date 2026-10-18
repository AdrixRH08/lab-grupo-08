def calcular_promedio(n1, n2, n3, n4):
    return (n1 + n2 + n3 + n4) / 4


def determinar_estado(promedio):
    if promedio < 11:
        return "DESAPROBADO"
    elif promedio <= 20:
        return "APROBADO"
    else:
        return "INVÁLIDO"