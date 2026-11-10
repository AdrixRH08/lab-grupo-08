"""Reportes de texto. Reporte es la clase base; cada subclase arma su propio texto (polimorfismo)."""
from __future__ import annotations

from abc import ABC, abstractmethod

from consultas import Estadisticas
from modelos import Registro


class Reporte(ABC):
    """Todo reporte se usa igual: reporte.generar(). Lo que cambia es el contenido."""

    @abstractmethod
    def generar(self) -> str:
        ...

    def __str__(self) -> str:
        return self.generar()


class ReporteAlumno(Reporte):
    """Reporte de un curso de un alumno, con su promedio general."""

    def __init__(self, registro: Registro):
        self._registro = registro

    def generar(self) -> str:
        r = self._registro
        alumno = r.alumno
        notas = "\n".join(f"Nota {i}: {nota}" for i, nota in enumerate(r.notas, start=1))
        return (
            f"{'=' * 20}\n"
            f"DNI: {alumno.dni}\n"
            f"Alumno: {alumno.nombre}\n"
            f"Curso: {r.curso}\n\n"
            f"{notas}\n\n"
            f"Promedio del curso: {r.promedio:.2f}\n"
            f"Estado: {r.estado}\n\n"
            f"Cursos registrados del alumno: {alumno.cantidad_cursos}\n"
            f"Promedio general: {alumno.promedio_general:.2f}\n"
            f"¡Gracias por usar el programa!\n\n"
            f"{'=' * 20}"
        )


class ReporteEstadisticas(Reporte):
    """Reporte con las estadísticas del salón (acepta None cuando todavía no hay alumnos)."""

    def __init__(self, estadisticas: Estadisticas | None):
        self._est = estadisticas

    def generar(self) -> str:
        est = self._est
        if est is None:
            return "Todavía no hay alumnos registrados."

        porcentaje = est.aprobados / est.total_registros * 100
        mejor, peor = est.mejor, est.peor
        lineas = [
            "=" * 34,
            "ESTADÍSTICAS DEL SALÓN",
            "=" * 34,
            f"Registros (alumno-curso): {est.total_registros}",
            f"Alumnos distintos: {est.total_alumnos}",
            f"Promedio general del salón: {est.promedio_salon:.2f}",
            "",
            f"Aprobados: {est.aprobados} ({porcentaje:.1f}%)",
            f"Desaprobados: {est.desaprobados}",
            "",
            f"Promedio más alto: {mejor.promedio:.2f} ({mejor.alumno.nombre} - {mejor.curso})",
            f"Promedio más bajo: {peor.promedio:.2f} ({peor.alumno.nombre} - {peor.curso})",
            "",
            "Promedio por curso:",
        ]
        lineas.extend(f"  - {curso}: {promedio:.2f}" for curso, promedio in est.promedios_curso.items())
        return "\n".join(lineas)
