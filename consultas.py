from validaciones import normalizar_texto


def buscar_por_dni(lista, dni):
    """Retorna los índices de todos los registros (cursos) de ese DNI."""
    return [i for i, registro in enumerate(lista) if registro["dni"] == dni]


def unificar_nombre_curso(lista, curso, ignorar=None):
    """Si el curso ya existe (sin importar mayúsculas, tildes o espacios), retorna su escritura original."""
    for i, registro in enumerate(lista):
        if i != ignorar and normalizar_texto(registro["curso"]) == normalizar_texto(curso):
            return registro["curso"]
    return " ".join(curso.split())


def unificar_nombre_alumno(lista, dni, nombre):
    """Si el DNI ya tiene registros, retorna el nombre con el que se registró por primera vez."""
    for registro in lista:
        if registro["dni"] == dni:
            return registro["user"]
    return " ".join(nombre.split())


def promedio_general_alumno(lista, dni):
    """Promedio de los promedios de todos los cursos del alumno. None si no existe."""
    indices = buscar_por_dni(lista, dni)
    if not indices:
        return None
    return sum(lista[i]["promedio"] for i in indices) / len(indices)


def calcular_estadisticas(lista):
    """Retorna un diccionario con las estadísticas del salón. None si no hay registros."""
    if not lista:
        return None

    total = len(lista)
    aprobados = sum(1 for r in lista if r["estado"] == "APROBADO")
    desaprobados = sum(1 for r in lista if r["estado"] == "DESAPROBADO")

    por_curso = {}
    for r in lista:
        clave = normalizar_texto(r["curso"])
        if clave not in por_curso:
            por_curso[clave] = {"nombre": r["curso"].strip(), "promedios": []}
        por_curso[clave]["promedios"].append(r["promedio"])

    promedios_curso = {
        datos["nombre"]: sum(datos["promedios"]) / len(datos["promedios"])
        for datos in por_curso.values()
    }

    return {
        "total_registros": total,
        "total_alumnos": len({r["dni"] for r in lista}),
        "promedio_salon": sum(r["promedio"] for r in lista) / total,
        "aprobados": aprobados,
        "desaprobados": desaprobados,
        "mejor": max(lista, key=lambda r: r["promedio"]),
        "peor": min(lista, key=lambda r: r["promedio"]),
        "promedios_curso": promedios_curso,
    }