"""Consultas de solo lectura sobre los registros: estadísticas del salón."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from logica import APROBADO, DESAPROBADO
from modelos import Registro


@dataclass(frozen=True)
class Estadisticas:
    total_registros: int
    total_alumnos: int
    promedio_salon: float
    aprobados: int
    desaprobados: int
    mejor: Registro
    peor: Registro
    promedios_curso: dict[str, float]


def calcular_estadisticas(registros: Iterable[Registro]) -> Estadisticas | None:
    """Calcula todo en UNA sola pasada. Retorna None si no hay registros."""
    total = 0
    suma = 0.0
    aprobados = desaprobados = 0
    dnis = set()
    mejor = peor = None
    por_curso = {}  # curso_clave -> [nombre, suma de promedios, cantidad]

    for r in registros:
        total += 1
        suma += r.promedio
        dnis.add(r.alumno.dni)
        if r.estado == APROBADO:
            aprobados += 1
        elif r.estado == DESAPROBADO:
            desaprobados += 1

        if mejor is None:
            mejor = peor = r
        else:
            if r.promedio > mejor.promedio:
                mejor = r
            if r.promedio < peor.promedio:
                peor = r

        datos = por_curso.get(r.curso_clave)
        if datos is None:
            por_curso[r.curso_clave] = [r.curso, r.promedio, 1]
        else:
            datos[1] += r.promedio
            datos[2] += 1

    if total == 0:
        return None

    return Estadisticas(
        total_registros=total,
        total_alumnos=len(dnis),
        promedio_salon=suma / total,
        aprobados=aprobados,
        desaprobados=desaprobados,
        mejor=mejor,
        peor=peor,
        promedios_curso={nombre: s / n for nombre, s, n in por_curso.values()},
    )
