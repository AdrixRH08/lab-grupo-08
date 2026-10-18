def construir_reporte(user, dni, curso, n1, n2, n3, n4, promedio, estado):
    return (
        f"{'='*20}\n"
        f"DNI: {dni}\n"
        f"Alumno: {user}\n"
        f"Curso: {curso}\n\n"
        f"Nota 1: {n1}\n"
        f"Nota 2: {n2}\n"
        f"Nota 3: {n3}\n"
        f"Nota 4: {n4}\n\n"
        f"Promedio de notas: {promedio:.2f}\n"
        f"Estado: {estado}\n"
        f"¡Gracias por usar el programa!\n\n"
        f"{'='*20}"
    )