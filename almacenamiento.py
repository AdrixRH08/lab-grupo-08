"""Persistencia. RepositorioNotas es la clase base; cada subclase decide DÓNDE se guardan las filas."""
from __future__ import annotations

import csv
import os
import warnings
from abc import ABC, abstractmethod
from typing import Iterable

from modelos import Alumno, Registro
from validaciones import validar_dni

ARCHIVO_ALUMNOS = "alumnos.csv"
ENCABEZADOS = ["dni", "user", "curso", "n1", "n2", "n3", "n4", "promedio", "estado"]


class RepositorioNotas(ABC):
    """Interfaz común. Cargar y guardar son iguales para todos; leer/escribir filas lo define cada subclase."""

    def cargar(self) -> list[Registro]:
        """Arma los objetos a partir de las filas. Las filas inválidas se omiten con un aviso."""
        alumnos: dict[str, Alumno] = {}
        registros: list[Registro] = []
        omitidas = 0
        for dni, nombre, curso, notas in self._leer_filas():
            try:
                dni = validar_dni(dni)
                alumno = alumnos.get(dni)
                if alumno is None:
                    alumno = Alumno(dni, nombre)
                registros.append(alumno.agregar_curso(curso, notas))
                alumnos[dni] = alumno
            except ValueError:  # ErrorValidacion también es ValueError
                omitidas += 1
        if omitidas:
            warnings.warn(f"Se omitieron {omitidas} fila(s) inválidas al cargar los alumnos.", stacklevel=2)
        return registros

    def guardar(self, registros: Iterable[Registro]) -> None:
        """Escribe TODOS los registros (promedio y estado salen de las notas)."""
        self._escribir_filas(
            (r.alumno.dni, r.alumno.nombre, r.curso, r.notas, r.promedio, r.estado)
            for r in registros
        )

    @abstractmethod
    def _leer_filas(self) -> Iterable[tuple]:
        """Devuelve tuplas (dni, nombre, curso, (n1, n2, n3, n4))."""

    @abstractmethod
    def _escribir_filas(self, filas: Iterable[tuple]) -> None:
        """Recibe tuplas (dni, nombre, curso, notas, promedio, estado)."""


class RepositorioCSV(RepositorioNotas):
    """Guarda en un archivo CSV (mismo formato de siempre)."""

    def __init__(self, ruta: str = ARCHIVO_ALUMNOS):
        self._ruta = ruta

    def _leer_filas(self):
        if not os.path.exists(self._ruta):
            return
        with open(self._ruta, mode="r", newline="", encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                yield (
                    fila.get("dni"), fila.get("user"), fila.get("curso"),
                    (fila.get("n1"), fila.get("n2"), fila.get("n3"), fila.get("n4")),
                )

    def _escribir_filas(self, filas):
        with open(self._ruta, mode="w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(ENCABEZADOS)
            for dni, nombre, curso, notas, promedio, estado in filas:
                escritor.writerow([dni, nombre, curso, *notas, promedio, estado])


class RepositorioMemoria(RepositorioNotas):
    """No toca el disco: sirve para demostraciones y pruebas. Misma interfaz, otro comportamiento."""

    def __init__(self):
        self._filas: list[tuple] = []

    def _leer_filas(self):
        return [(dni, nombre, curso, notas) for dni, nombre, curso, notas, _, _ in self._filas]

    def _escribir_filas(self, filas):
        self._filas = list(filas)
