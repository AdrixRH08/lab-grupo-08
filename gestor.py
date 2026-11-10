from __future__ import annotations

from almacenamiento import RepositorioNotas
from consultas import Estadisticas, calcular_estadisticas
from modelos import Alumno, Registro
from validaciones import (
    ErrorCursoDuplicado, ErrorValidacion, normalizar_texto,
    validar_dni, validar_notas, validar_texto_obligatorio,
)


class GestorNotas:

    def __init__(self, repositorio: RepositorioNotas):
        self._repo = repositorio
        self._registros: list[Registro] = repositorio.cargar()
        self._alumnos: dict[str, Alumno] = {r.alumno.dni: r.alumno for r in self._registros}

    def __len__(self) -> int:
        return len(self._registros)

    @property
    def registros(self) -> tuple[Registro, ...]:
        return tuple(self._registros)

    # --- consultas ----------------------------------------------------------
    def buscar_por_dni(self, dni: str) -> list[Registro]:
        """Todos los cursos de ese DNI (lista vacía si no existe). Lanza ErrorValidacion si el DNI es inválido."""
        alumno = self._alumnos.get(validar_dni(dni))
        return list(alumno.registros) if alumno else []

    def estadisticas(self) -> Estadisticas | None:
        return calcular_estadisticas(self._registros)

    # --- operaciones --------------------------------------------------------
    def registrar(self, dni: str, nombre: str, curso: str, notas) -> Registro:
        # Mismo orden de validación que siempre: nombre, curso, DNI, notas.
        nombre = validar_texto_obligatorio(nombre, "Nombre")
        curso = validar_texto_obligatorio(curso, "Curso")
        dni = validar_dni(dni)
        notas = validar_notas(notas)

        alumno = self._alumnos.get(dni)
        clave_nombre = normalizar_texto(nombre)
        if alumno is not None and alumno.nombre_clave != clave_nombre:
            raise ErrorValidacion("Ese DNI ya está registrado con otro nombre.")
        if self._nombre_en_uso(clave_nombre, excepto_dni=dni):
            raise ErrorValidacion("Ese nombre ya está registrado con otro DNI.")
        if alumno is not None and alumno.buscar_curso(curso) is not None:
            raise ErrorCursoDuplicado("Ese alumno ya tiene registrado ese curso.")

        if alumno is None:           # si el DNI ya existía se reutiliza su objeto (y su nombre)
            alumno = Alumno(dni, nombre)
            self._alumnos[dni] = alumno
        registro = alumno.agregar_curso(self._unificar_curso(curso), notas)
        self._registros.append(registro)
        self._repo.guardar(self._registros)
        return registro

    def editar(self, registro: Registro, nombre: str, curso: str, notas) -> None:
        nombre = validar_texto_obligatorio(nombre, "Nombre")
        curso = validar_texto_obligatorio(curso, "Curso")
        notas = validar_notas(notas)

        alumno = registro.alumno
        if self._nombre_en_uso(normalizar_texto(nombre), excepto_dni=alumno.dni):
            raise ErrorValidacion("Ese nombre ya pertenece a otro alumno (otro DNI).")
        if alumno.buscar_curso(curso, ignorar=registro) is not None:
            raise ErrorCursoDuplicado("Ese alumno ya tiene registrado ese curso.")

        registro.curso = self._unificar_curso(curso, ignorar=registro)
        registro.notas = notas
        alumno.nombre = nombre 
        self._repo.guardar(self._registros)

    def eliminar(self, registro: Registro) -> None:
        self._registros.remove(registro)
        alumno = registro.alumno
        alumno.quitar_registro(registro)
        if alumno.cantidad_cursos == 0:
            del self._alumnos[alumno.dni]
        self._repo.guardar(self._registros)

    def _nombre_en_uso(self, clave_nombre: str, excepto_dni: str) -> bool:
        return any(
            a.nombre_clave == clave_nombre
            for dni, a in self._alumnos.items() if dni != excepto_dni
        )

    def _unificar_curso(self, curso: str, ignorar: Registro | None = None) -> str:
        clave = normalizar_texto(curso)
        for r in self._registros:
            if r is not ignorar and r.curso_clave == clave:
                return r.curso
        return curso
