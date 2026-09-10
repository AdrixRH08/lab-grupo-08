import csv
import os

ARCHIVO_ALUMNOS = "alumnos.csv"

def guardar_alumnos(lista_alumnos):
    """Sin retorno: escribe TODA la lista de alumnos en el archivo CSV."""
    with open(ARCHIVO_ALUMNOS, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["dni", "user", "curso", "n1", "n2", "n3", "n4", "promedio", "estado"])
        for alumno in lista_alumnos:
            escritor.writerow([
                alumno["dni"], alumno["user"], alumno["curso"],
                alumno["notas"][0], alumno["notas"][1], alumno["notas"][2], alumno["notas"][3],
                alumno["promedio"], alumno["estado"]
            ])


def cargar_alumnos():
    """Con retorno: lee el archivo (si existe) y devuelve la lista de alumnos."""
    lista = []
    if not os.path.exists(ARCHIVO_ALUMNOS):
        return lista  # todavía no hay archivo, devuelve lista vacía

    with open(ARCHIVO_ALUMNOS, mode="r", newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            alumno = {
                "dni": int(fila["dni"]),
                "user": fila["user"],
                "curso": fila["curso"],
                "notas": [int(fila["n1"]), int(fila["n2"]), int(fila["n3"]), int(fila["n4"])],
                "promedio": float(fila["promedio"]),
                "estado": fila["estado"],
            }
            lista.append(alumno)
    return lista