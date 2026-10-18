def buscar_por_dni(lista, dni):
    """Retorna los índices de todos los registros (cursos) de ese DNI."""
    return [i for i, registro in enumerate(lista) if registro["dni"] == dni]


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
        clave = r["curso"].strip().lower()
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