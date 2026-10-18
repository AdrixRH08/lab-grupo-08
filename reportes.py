def construir_reporte(registro, promedio_general, cantidad_cursos):
    notas = registro["notas"]
    return (
        f"{'='*20}\n"
        f"DNI: {registro['dni']}\n"
        f"Alumno: {registro['user']}\n"
        f"Curso: {registro['curso']}\n\n"
        f"Nota 1: {notas[0]}\n"
        f"Nota 2: {notas[1]}\n"
        f"Nota 3: {notas[2]}\n"
        f"Nota 4: {notas[3]}\n\n"
        f"Promedio del curso: {registro['promedio']:.2f}\n"
        f"Estado: {registro['estado']}\n\n"
        f"Cursos registrados del alumno: {cantidad_cursos}\n"
        f"Promedio general: {promedio_general:.2f}\n"
        f"¡Gracias por usar el programa!\n\n"
        f"{'='*20}"
    )


def construir_reporte_estadisticas(est):
    if est is None:
        return "Todavía no hay alumnos registrados."

    porcentaje = est["aprobados"] / est["total_registros"] * 100
    mejor = est["mejor"]
    peor = est["peor"]

    lineas = [
        "=" * 34,
        "ESTADÍSTICAS DEL SALÓN",
        "=" * 34,
        f"Registros (alumno-curso): {est['total_registros']}",
        f"Alumnos distintos: {est['total_alumnos']}",
        f"Promedio general del salón: {est['promedio_salon']:.2f}",
        "",
        f"Aprobados: {est['aprobados']} ({porcentaje:.1f}%)",
        f"Desaprobados: {est['desaprobados']}",
        "",
        f"Promedio más alto: {mejor['promedio']:.2f} ({mejor['user']} - {mejor['curso']})",
        f"Promedio más bajo: {peor['promedio']:.2f} ({peor['user']} - {peor['curso']})",
        "",
        "Promedio por curso:",
    ]
    for curso, promedio in est["promedios_curso"].items():
        lineas.append(f"  - {curso}: {promedio:.2f}")
    return "\n".join(lineas)