import tkinter as tk
from tkinter import ttk, messagebox

from logica import crear_registro
from validaciones import (
    validar_texto_obligatorio, validar_nota, validar_dni, convertir_notas,
    curso_ya_registrado, nombre_coincide,
)
from reportes import construir_reporte, construir_reporte_estadisticas
from consultas import buscar_por_dni, promedio_general_alumno, calcular_estadisticas
from almacenamiento import guardar_alumnos, cargar_alumnos

lista_alumnos = cargar_alumnos()


# ---------------------------------------------------------
# Validaciones con mensaje (usan messagebox, por eso viven aquí)
# ---------------------------------------------------------
def validar_textos(user, curso, parent=None):
    if not validar_texto_obligatorio(user):
        messagebox.showerror("Error", "El campo 'Nombre' no puede estar vacío.", parent=parent)
        return False
    if not validar_texto_obligatorio(curso):
        messagebox.showerror("Error", "El campo 'Curso' no puede estar vacío.", parent=parent)
        return False
    return True


def validar_notas_ingresadas(textos, parent=None):
    """Retorna la lista de 4 notas enteras, o None (mostrando el error) si alguna es inválida."""
    notas = convertir_notas(textos)
    if notas is None:
        messagebox.showerror("Error", "Las notas deben ser números enteros.", parent=parent)
        return None
    for nota in notas:
        if not validar_nota(nota):
            messagebox.showerror("Error", "Las notas deben estar entre 0 y 20.", parent=parent)
            return None
    return notas


# ---------------------------------------------------------
# Funciones de la interfaz
# ---------------------------------------------------------
def mostrar_reporte(texto):
    txt_resultado.delete("1.0", tk.END)
    txt_resultado.insert(tk.END, texto)


def limpiar_curso_y_notas():
    for entrada in [entry_curso, *entradas_notas]:
        entrada.delete(0, tk.END)


def limpiar_todo():
    for entrada in [entry_user, entry_dni, entry_curso, *entradas_notas]:
        entrada.delete(0, tk.END)
    txt_resultado.delete("1.0", tk.END)


def actualizar_tabla(indices=None):
    for fila in tabla.get_children():
        tabla.delete(fila)
    if indices is None:
        indices = range(len(lista_alumnos))
    for i in indices:
        r = lista_alumnos[i]
        tabla.insert("", "end", iid=str(i), values=(
            r["dni"], r["user"], r["curso"], *r["notas"],
            f"{r['promedio']:.2f}", r["estado"],
        ))


def actualizar_estadisticas():
    texto = construir_reporte_estadisticas(calcular_estadisticas(lista_alumnos))
    txt_estadisticas.config(state="normal")
    txt_estadisticas.delete("1.0", tk.END)
    txt_estadisticas.insert(tk.END, texto)
    txt_estadisticas.config(state="disabled")


def registrar_alumno():
    user = entry_user.get().strip()
    dni = entry_dni.get().strip()
    curso = entry_curso.get().strip()

    if not validar_textos(user, curso):
        return
    if not validar_dni(dni):
        messagebox.showerror("Error", "El DNI debe tener exactamente 8 dígitos numéricos.")
        return
    notas = validar_notas_ingresadas([entrada.get() for entrada in entradas_notas])
    if notas is None:
        return
    if not nombre_coincide(lista_alumnos, dni, user):
        messagebox.showerror("Error", "Ese DNI ya está registrado con otro nombre.")
        return
    if curso_ya_registrado(lista_alumnos, dni, curso):
        messagebox.showerror(
            "Error",
            "Ese alumno ya tiene registrado ese curso.\nUsa la pestaña 'Alumnos' para editarlo."
        )
        return

    registro = crear_registro(dni, user, curso, notas)
    lista_alumnos.append(registro)
    guardar_alumnos(lista_alumnos)

    cantidad_cursos = len(buscar_por_dni(lista_alumnos, dni))
    promedio_general = promedio_general_alumno(lista_alumnos, dni)
    mostrar_reporte(construir_reporte(registro, promedio_general, cantidad_cursos))

    mostrar_todos()
    actualizar_estadisticas()
    limpiar_curso_y_notas()


def buscar_alumno():
    dni = entry_buscar.get().strip()
    if not validar_dni(dni):
        messagebox.showerror("Error", "El DNI debe tener exactamente 8 dígitos numéricos.")
        return
    indices = buscar_por_dni(lista_alumnos, dni)
    if not indices:
        messagebox.showinfo("Búsqueda", "No se encontró ningún alumno con ese DNI.")
        return
    actualizar_tabla(indices)
    promedio = promedio_general_alumno(lista_alumnos, dni)
    nombre = lista_alumnos[indices[0]]["user"]
    lbl_resumen.config(text=f"{nombre} | {len(indices)} curso(s) | Promedio general: {promedio:.2f}")


def mostrar_todos():
    entry_buscar.delete(0, tk.END)
    lbl_resumen.config(text="")
    actualizar_tabla()


def obtener_indice_seleccionado():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Atención", "Selecciona un registro de la tabla.")
        return None
    return int(seleccion[0])


def eliminar_seleccionado():
    indice = obtener_indice_seleccionado()
    if indice is None:
        return
    r = lista_alumnos[indice]
    if messagebox.askyesno("Confirmar", f"¿Eliminar el curso '{r['curso']}' de {r['user']}?"):
        lista_alumnos.pop(indice)
        guardar_alumnos(lista_alumnos)
        mostrar_todos()
        actualizar_estadisticas()


def editar_seleccionado():
    indice = obtener_indice_seleccionado()
    if indice is None:
        return
    r = lista_alumnos[indice]

    dialogo = tk.Toplevel(ventana)
    dialogo.title("Editar registro")
    dialogo.geometry("340x440")
    dialogo.transient(ventana)
    dialogo.grab_set()

    tk.Label(dialogo, text=f"DNI: {r['dni']} (no editable)").pack(pady=6)
    e_user = crear_campo(dialogo, "Nombre (se aplica a todos sus cursos):")
    e_user.insert(0, r["user"])
    e_curso = crear_campo(dialogo, "Curso:")
    e_curso.insert(0, r["curso"])
    e_notas = []
    for k in range(4):
        entrada = crear_campo(dialogo, f"Nota {k + 1}:")
        entrada.insert(0, str(r["notas"][k]))
        e_notas.append(entrada)

    def guardar_cambios():
        user = e_user.get().strip()
        curso = e_curso.get().strip()
        if not validar_textos(user, curso, parent=dialogo):
            return
        notas = validar_notas_ingresadas([e.get() for e in e_notas], parent=dialogo)
        if notas is None:
            return
        if curso_ya_registrado(lista_alumnos, r["dni"], curso, ignorar=indice):
            messagebox.showerror("Error", "Ese alumno ya tiene registrado ese curso.", parent=dialogo)
            return

        lista_alumnos[indice] = crear_registro(r["dni"], user, curso, notas)
        for otro in lista_alumnos:
            if otro["dni"] == r["dni"]:
                otro["user"] = user
        guardar_alumnos(lista_alumnos)
        dialogo.destroy()
        mostrar_todos()
        actualizar_estadisticas()

    tk.Button(dialogo, text="Guardar cambios", command=guardar_cambios).pack(pady=12)


def crear_campo(padre, texto):
    tk.Label(padre, text=texto).pack(pady=2)
    entrada = tk.Entry(padre)
    entrada.pack(fill="x", padx=20, pady=2)
    return entrada


# ---------------------------------------------------------
# Construcción de la ventana
# ---------------------------------------------------------
ventana = tk.Tk()
ventana.title("Sistema de Gestión de Notas y Rendimiento Académico")
ventana.geometry("820x660")

pestanas = ttk.Notebook(ventana)
pestanas.pack(fill="both", expand=True, padx=8, pady=8)

# --- Pestaña 1: Registrar ---
frame_registro = ttk.Frame(pestanas)
pestanas.add(frame_registro, text="Registrar")

entry_user = crear_campo(frame_registro, "Nombre del alumno:")
entry_dni = crear_campo(frame_registro, "DNI (8 dígitos):")
entry_curso = crear_campo(frame_registro, "Curso:")
entradas_notas = [crear_campo(frame_registro, f"Nota {k}:") for k in range(1, 5)]

frame_botones = ttk.Frame(frame_registro)
frame_botones.pack(pady=8)
tk.Button(frame_botones, text="Registrar y mostrar reporte", command=registrar_alumno).pack(side="left", padx=6)
tk.Button(frame_botones, text="Limpiar todo", command=limpiar_todo).pack(side="left", padx=6)

txt_resultado = tk.Text(frame_registro, height=14, font=("Courier", 10))
txt_resultado.pack(fill="both", expand=True, padx=20, pady=5)

# --- Pestaña 2: Alumnos ---
frame_alumnos = ttk.Frame(pestanas)
pestanas.add(frame_alumnos, text="Alumnos")

frame_busqueda = ttk.Frame(frame_alumnos)
frame_busqueda.pack(fill="x", padx=10, pady=8)
tk.Label(frame_busqueda, text="Buscar por DNI:").pack(side="left")
entry_buscar = tk.Entry(frame_busqueda, width=14)
entry_buscar.pack(side="left", padx=6)
tk.Button(frame_busqueda, text="Buscar", command=buscar_alumno).pack(side="left", padx=4)
tk.Button(frame_busqueda, text="Mostrar todos", command=mostrar_todos).pack(side="left", padx=4)

lbl_resumen = tk.Label(frame_alumnos, text="", font=("Arial", 10, "bold"))
lbl_resumen.pack(anchor="w", padx=12)

columnas = ("dni", "alumno", "curso", "n1", "n2", "n3", "n4", "promedio", "estado")
encabezados = ("DNI", "Alumno", "Curso", "N1", "N2", "N3", "N4", "Promedio", "Estado")
anchos = (85, 140, 120, 40, 40, 40, 40, 70, 110)

tabla = ttk.Treeview(frame_alumnos, columns=columnas, show="headings", height=16)
for columna, encabezado, ancho in zip(columnas, encabezados, anchos):
    tabla.heading(columna, text=encabezado)
    tabla.column(columna, width=ancho, anchor="center")
tabla.pack(fill="both", expand=True, padx=10, pady=6)

frame_acciones = ttk.Frame(frame_alumnos)
frame_acciones.pack(pady=8)
tk.Button(frame_acciones, text="Editar seleccionado", command=editar_seleccionado).pack(side="left", padx=6)
tk.Button(frame_acciones, text="Eliminar seleccionado", command=eliminar_seleccionado).pack(side="left", padx=6)

# --- Pestaña 3: Estadísticas ---
frame_estadisticas = ttk.Frame(pestanas)
pestanas.add(frame_estadisticas, text="Estadísticas")

txt_estadisticas = tk.Text(frame_estadisticas, height=24, font=("Courier", 10), state="disabled")
txt_estadisticas.pack(fill="both", expand=True, padx=20, pady=10)
tk.Button(frame_estadisticas, text="Actualizar", command=actualizar_estadisticas).pack(pady=6)

actualizar_tabla()
actualizar_estadisticas()

ventana.mainloop()