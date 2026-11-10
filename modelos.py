"""Clases del dominio.

    Persona          (clase base: DNI + nombre)
      └── Alumno     (hereda de Persona y agrega sus cursos)
    Registro         (un curso de un alumno: 4 notas, promedio y estado)
"""
from __future__ import annotations

from logica import calcular_promedio, determinar_estado
from validaciones import (
    normalizar_texto, validar_dni, validar_notas, validar_texto_obligatorio,
)


class Persona:
    """Clase base. El DNI es de solo lectura; el nombre es editable pero siempre validado."""

    def __init__(self, dni: str, nombre: str):
        self._dni = validar_dni(dni)
        self.nombre = nombre  # pasa por el setter, que valida

    # --- getters y setters --------------------------------------------------
    @property
    def dni(self) -> str:
        """Getter sin setter: el DNI no se puede cambiar una vez creada la persona."""
        return self._dni

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = validar_texto_obligatorio(valor, "Nombre")
        self._nombre_clave = normalizar_texto(self._nombre)  # se calcula una sola vez

    @property
    def nombre_clave(self) -> str:
        """Nombre normalizado (sin tildes ni mayúsculas) para comparar rápido."""
        return self._nombre_clave

    # --- polimorfismo: las subclases pueden redefinir descripcion() ---------
    def descripcion(self) -> str:
        return f"{self.nombre} (DNI {self.dni})"

    def __str__(self) -> str:
        return self.descripcion()


class Alumno(Persona):
    """Una Persona que lleva cursos. Hereda dni y nombre; agrega los registros de sus cursos."""

    def __init__(self, dni: str, nombre: str):
        super().__init__(dni, nombre)
        self._registros: list[Registro] = []

    @property
    def registros(self) -> tuple[Registro, ...]:
        """Copia de solo lectura: para agregar o quitar cursos se usan los métodos de abajo."""
        return tuple(self._registros)

    @property
    def cantidad_cursos(self) -> int:
        return len(self._registros)

    @property
    def promedio_general(self) -> float | None:
        """Promedio de los promedios de todos sus cursos (None si no tiene cursos)."""
        if not self._registros:
            return None
        return sum(r.promedio for r in self._registros) / len(self._registros)

    def agregar_curso(self, curso: str, notas) -> Registro:
        registro = Registro(self, curso, notas)
        self._registros.append(registro)
        return registro

    def quitar_registro(self, registro: Registro) -> None:
        self._registros.remove(registro)

    def buscar_curso(self, curso: str, ignorar: Registro | None = None) -> Registro | None:
        """Busca un curso ya registrado (sin importar mayúsculas, tildes ni espacios)."""
        clave = normalizar_texto(curso)
        for registro in self._registros:
            if registro is not ignorar and registro.curso_clave == clave:
                return registro
        return None

    # polimorfismo: redefine el método de Persona reutilizándolo con super()
    def descripcion(self) -> str:
        return f"{super().descripcion()} - {self.cantidad_cursos} curso(s)"


class Registro:
    """Un curso de un alumno. El promedio y el estado se derivan de las notas (solo lectura)."""

    def __init__(self, alumno: Alumno, curso: str, notas):
        self._alumno = alumno
        self.curso = curso   # setter
        self.notas = notas   # setter (también recalcula promedio y estado)

    @property
    def alumno(self) -> Alumno:
        return self._alumno

    @property
    def curso(self) -> str:
        return self._curso

    @curso.setter
    def curso(self, valor: str) -> None:
        self._curso = validar_texto_obligatorio(valor, "Curso")
        self._curso_clave = normalizar_texto(self._curso)

    @property
    def curso_clave(self) -> str:
        return self._curso_clave

    @property
    def notas(self) -> tuple[int, ...]:
        """Tupla (inmutable): no se puede modificar por fuera del setter."""
        return self._notas

    @notas.setter
    def notas(self, valores) -> None:
        self._notas = validar_notas(valores)
        self._promedio = calcular_promedio(self._notas)   # una vez, no en cada lectura
        self._estado = determinar_estado(self._promedio)

    @property
    def promedio(self) -> float:
        return self._promedio

    @property
    def estado(self) -> str:
        return self._estado

    def __str__(self) -> str:
        return f"{self._alumno.nombre} - {self._curso}: {self._promedio:.2f} ({self._estado})"
