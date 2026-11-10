import os
import tempfile

from almacenamiento import RepositorioCSV, RepositorioMemoria
from gestor import GestorNotas
from modelos import Alumno, Persona
from reportes import ReporteAlumno, ReporteEstadisticas
from validaciones import ErrorValidacion


def mostrar_menu():
    print("1. Registrar notas")
    print("2. Consultar resultado")


def intentar_modificar_valor(x):
    x = x + 10
    return x


def agregar_nota_extra(lista_notas):
    lista_notas.append(0)


def demostrar_valor_y_referencia():
    numero_original = 5
    numero_resultado = intentar_modificar_valor(numero_original)
    print("--- Paso por VALOR (int) ---")
    print(f"Antes de llamar la función:  numero_original = {numero_original}")
    print(f"Valor retornado por la función: {numero_resultado}")
    print(f"Después de llamar la función: numero_original = {numero_original}  "
          f"(NO cambió, porque los int son inmutables)\n")

    notas_originales = [15, 12, 18]
    print("--- Paso por REFERENCIA (lista) ---")
    print(f"Antes de llamar la función:  notas_originales = {notas_originales}")
    agregar_nota_extra(notas_originales)
    print(f"Después de llamar la función: notas_originales = {notas_originales}  "
          f"(SÍ cambió, porque las listas son mutables)\n")


def demostrar_poo():
    """Getters/setters, herencia y polimorfismo en consola (sin interfaz gráfica)."""
    gestor = GestorNotas(RepositorioMemoria())
    registro = gestor.registrar("12345678", "ana   perez", "Matemática", ["15", "12", "18", "10"])
    alumno = registro.alumno

    print("--- GETTERS Y SETTERS (@property) ---")
    print(f"Getter nombre:   {alumno.nombre!r}  (el setter ya limpió los espacios)")
    alumno.nombre = "  Ana   Pérez "
    print(f"Setter nombre:   {alumno.nombre!r}")
    for intento in (lambda: setattr(registro, "notas", (25, 0, 0, 0)),
                    lambda: setattr(alumno, "nombre", "   ")):
        try:
            intento()
        except ErrorValidacion as error:
            print(f"Setter rechaza un valor inválido: {error}")
    try:
        registro.promedio = 20
    except AttributeError:
        print(f"'promedio' es solo lectura (se calcula de las notas): {registro.promedio}")
    registro.notas = (20, 20, 20, 20)
    print(f"Tras cambiar las notas con el setter, el promedio es {registro.promedio} y el estado {registro.estado}\n")

    print("--- HERENCIA ---")
    print(f"Alumno hereda de Persona: {issubclass(Alumno, Persona)}  |  MRO: "
          f"{[c.__name__ for c in Alumno.__mro__]}\n")

    print("--- POLIMORFISMO ---")
    print("1) Mismo método, distinto resultado según la clase:")
    for persona in (Persona("87654321", "Luis Ramos"), alumno):
        print(f"   {type(persona).__name__:<8} -> {persona.descripcion()}")
    print("2) Mismo generar() para cualquier Reporte:")
    for reporte in (ReporteAlumno(registro), ReporteEstadisticas(gestor.estadisticas())):
        print(f"   {type(reporte).__name__:<20} -> {len(reporte.generar().splitlines())} líneas")
    print("3) Mismo código con cualquier RepositorioNotas:")
    with tempfile.TemporaryDirectory() as carpeta:
        for repositorio in (RepositorioMemoria(), RepositorioCSV(os.path.join(carpeta, "demo.csv"))):
            g = GestorNotas(repositorio)
            g.registrar("11111111", "Demo", "Curso", ["10", "11", "12", "13"])
            print(f"   {type(repositorio).__name__:<18} -> {len(GestorNotas(repositorio))} registro(s) guardado(s)")


if __name__ == "__main__":
    mostrar_menu()
    demostrar_valor_y_referencia()
    demostrar_poo()
