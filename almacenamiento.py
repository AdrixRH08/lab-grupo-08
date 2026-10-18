import csv
import os

ARCHIVO_ALUMNOS = "alumnos.csv"
ENCABEZADOS = ["dni", "user", "curso", "n1", "n2", "n3", "n4", "promedio", "estado"]


def guardar_alumnos(lista_alumnos):
    """Sin retorno: escribe TODA la lista de registros en el archivo CSV."""
    with open(ARCHIVO_ALUMNOS, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(ENCABEZADOS)
        for r in lista_alumnos:
            escritor.writerow([
                r["dni"], r["user"], r["curso"],
                r["notas"][0], r["notas"][1], r["notas"][2], r["notas"][3],
                r["promedio"], r["estado"],
            ])


def cargar_alumnos():
    """Con retorno: lee el CSV (si existe) y devuelve la lista de registros."""
    lista = []
    if not os.path.exists(ARCHIVO_ALUMNOS):
        return lista

    with open(ARCHIVO_ALUMNOS, mode="r", newline="", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            try:
                lista.append({
                    "dni": fila["dni"],
                    "user": fila["user"],
                    "curso": fila["curso"],
                    "notas": [int(fila["n1"]), int(fila["n2"]), int(fila["n3"]), int(fila["n4"])],
                    "promedio": float(fila["promedio"]),
                    "estado": fila["estado"],
                })
            except (KeyError, ValueError):
                continue
    return lista