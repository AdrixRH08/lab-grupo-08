"""Interfaz gráfica (Tkinter) del Sistema de Gestión de Notas y Rendimiento Académico.

Solo dibuja la ventana y muestra los errores: las reglas viven en GestorNotas y los modelos.
"""
import tkinter as tk
from tkinter import messagebox, ttk

from almacenamiento import RepositorioCSV
from gestor import GestorNotas
from reportes import Reporte, ReporteAlumno, ReporteEstadisticas
from validaciones import ErrorCursoDuplicado, ErrorValidacion


# ---------------------------------------------------------
# Funciones auxiliares de la interfaz
# ---------------------------------------------------------
def crear_campo(padre, texto):
    tk.Label(padre, text=texto).pack(pady=2)
    entrada = tk.Entry(padre)
    entrada.pack(fill="x", padx=20, pady=2)
    return entrada


def vaciar(entradas):
    for entrada in entradas:
        entrada.delete(0, tk.END)


# ---------------------------------------------------------
# Ventana de edición (hereda de Toplevel)
# ---------------------------------------------------------
class DialogoEdicion(tk.Toplevel):
    def __init__(self, ventana, gestor, registro, al_guardar):
        super().__init__(ventana)
        self._gestor = gestor
        self._registro = registro
        self._al_guardar = al_guardar

        self.title("Editar registro")
        self.geometry("340x440")
        self.transient(ventana)
        self.grab_set()

        tk.Label(self, text=f"DNI: {registro.alumno.dni} (no editable)").pack(pady=6)
        self._e_user = crear_campo(self, "Nombre (se aplica a todos sus cursos):")
        self._e_user.insert(0, registro.alumno.nombre)
        self._e_curso = crear_campo(self, "Curso:")
        self._e_curso.insert(0, registro.curso)
        self._e_notas = []
        for k, nota in enumerate(registro.notas, start=1):
            entrada = crear_campo(self, f"Nota {k}:")
            entrada.insert(0, str(nota))
            self._e_notas.append(entrada)

        tk.Button(self, text="Guardar cambios", command=self._guardar).pack(pady=12)

    def _guardar(self):
        try:
            self._gestor.editar(
                self._registro,
                self._e_user.get().strip(),
                self._e_curso.get().strip(),
                [e.get() for e in self._e_notas],
            )
        except ErrorValidacion as error:
            messagebox.showerror("Error", str(error), parent=self)
            return
        self.destroy()
        self._al_guardar()

class AppNotas(tk.Tk):
    COLUMNAS = ("dni", "alumno", "curso", "n1", "n2", "n3", "n4", "promedio", "estado")
    ENCABEZADOS = ("DNI", "Alumno", "Curso", "N1", "N2", "N3", "N4", "Promedio", "Estado")
    ANCHOS = (85, 140, 120, 40, 40, 40, 40, 70, 110)

    def __init__(self, gestor):
        super().__init__()
        self.gestor = gestor
        self._registro_por_iid = {} 

        self.title("Sistema de Gestión de Notas y Rendimiento Académico")
        self.geometry("820x660")

        pestanas = ttk.Notebook(self)
        pestanas.pack(fill="both", expand=True, padx=8, pady=8)
        self._construir_pestana_registro(pestanas)
        self._construir_pestana_alumnos(pestanas)
        self._construir_pestana_estadisticas(pestanas)

        self.actualizar_tabla()
        self.actualizar_estadisticas()

    def _construir_pestana_registro(self, pestanas):
        frame = ttk.Frame(pestanas)
        pestanas.add(frame, text="Registrar")

        self.entry_user = crear_campo(frame, "Nombre del alumno:")
        self.entry_dni = crear_campo(frame, "DNI (8 dígitos):")
        self.entry_curso = crear_campo(frame, "Curso:")
        self.entradas_notas = [crear_campo(frame, f"Nota {k}:") for k in range(1, 5)]

        botones = ttk.Frame(frame)
        botones.pack(pady=8)
        ttk.Button(botones, text="Registrar y mostrar reporte", command=self.registrar_alumno).pack(side="left", padx=6)
        ttk.Button(botones, text="Limpiar todo", command=self.limpiar_todo).pack(side="left", padx=6)

        self.txt_resultado = tk.Text(frame, height=14, font=("Courier", 10))
        self.txt_resultado.pack(fill="both", expand=True, padx=20, pady=5)

    def _construir_pestana_alumnos(self, pestanas):
        frame = ttk.Frame(pestanas)
        pestanas.add(frame, text="Alumnos")

        busqueda = ttk.Frame(frame)
        busqueda.pack(fill="x", padx=10, pady=8)
        tk.Label(busqueda, text="Buscar por DNI:").pack(side="left")
        self.entry_buscar = tk.Entry(busqueda, width=14)
        self.entry_buscar.pack(side="left", padx=6)
        ttk.Button(busqueda, text="Buscar", command=self.buscar_alumno).pack(side="left", padx=4)
        ttk.Button(busqueda, text="Mostrar todos", command=self.mostrar_todos).pack(side="left", padx=4)

        self.lbl_resumen = tk.Label(frame, text="", font=("Arial", 10, "bold"))
        self.lbl_resumen.pack(anchor="w", padx=12)

        self.tabla = ttk.Treeview(frame, columns=self.COLUMNAS, show="headings", height=16)
        for columna, encabezado, ancho in zip(self.COLUMNAS, self.ENCABEZADOS, self.ANCHOS):
            self.tabla.heading(columna, text=encabezado)
            self.tabla.column(columna, width=ancho, anchor="center")
        self.tabla.pack(fill="both", expand=True, padx=10, pady=6)

        acciones = ttk.Frame(frame)
        acciones.pack(pady=8)
        ttk.Button(acciones, text="Editar seleccionado", command=self.editar_seleccionado).pack(side="left", padx=6)
        ttk.Button(acciones, text="Eliminar seleccionado", command=self.eliminar_seleccionado).pack(side="left", padx=6)

    def _construir_pestana_estadisticas(self, pestanas):
        frame = ttk.Frame(pestanas)
        pestanas.add(frame, text="Estadísticas")

        self.txt_estadisticas = tk.Text(frame, height=24, font=("Courier", 10), state="disabled")
        self.txt_estadisticas.pack(fill="both", expand=True, padx=20, pady=10)
        ttk.Button(frame, text="Actualizar", command=self.actualizar_estadisticas).pack(pady=6)

    # --- mostrar información ----------------------------------------------
    def mostrar_reporte(self, reporte: Reporte):
        self.txt_resultado.delete("1.0", tk.END)
        self.txt_resultado.insert(tk.END, reporte.generar())

    def actualizar_estadisticas(self):
        reporte = ReporteEstadisticas(self.gestor.estadisticas())
        self.txt_estadisticas.config(state="normal")
        self.txt_estadisticas.delete("1.0", tk.END)
        self.txt_estadisticas.insert(tk.END, reporte.generar())
        self.txt_estadisticas.config(state="disabled")

    def actualizar_tabla(self, registros=None):
        self.tabla.delete(*self.tabla.get_children())
        self._registro_por_iid.clear()
        if registros is None:
            registros = self.gestor.registros
        for i, r in enumerate(registros):
            iid = str(i)
            self._registro_por_iid[iid] = r
            self.tabla.insert("", "end", iid=iid, values=(
                r.alumno.dni, r.alumno.nombre, r.curso, *r.notas,
                f"{r.promedio:.2f}", r.estado,
            ))

    def mostrar_todos(self):
        self.entry_buscar.delete(0, tk.END)
        self.lbl_resumen.config(text="")
        self.actualizar_tabla()

    def _refrescar(self):
        self.mostrar_todos()
        self.actualizar_estadisticas()

    def limpiar_curso_y_notas(self):
        vaciar([self.entry_curso, *self.entradas_notas])

    def limpiar_todo(self):
        vaciar([self.entry_user, self.entry_dni, self.entry_curso, *self.entradas_notas])
        self.txt_resultado.delete("1.0", tk.END)

    # --- acciones de los botones ------------------------------------------
    def registrar_alumno(self):
        try:
            registro = self.gestor.registrar(
                dni=self.entry_dni.get().strip(),
                nombre=self.entry_user.get().strip(),
                curso=self.entry_curso.get().strip(),
                notas=[entrada.get() for entrada in self.entradas_notas],
            )
        except ErrorCursoDuplicado as error:
            messagebox.showerror("Error", f"{error}\nUsa la pestaña 'Alumnos' para editarlo.")
            return
        except ErrorValidacion as error:
            messagebox.showerror("Error", str(error))
            return

        self.mostrar_reporte(ReporteAlumno(registro))
        self._refrescar()
        self.limpiar_curso_y_notas()

    def buscar_alumno(self):
        try:
            registros = self.gestor.buscar_por_dni(self.entry_buscar.get().strip())
        except ErrorValidacion as error:
            messagebox.showerror("Error", str(error))
            return
        if not registros:
            messagebox.showinfo("Búsqueda", "No se encontró ningún alumno con ese DNI.")
            return

        self.actualizar_tabla(registros)
        alumno = registros[0].alumno
        self.lbl_resumen.config(
            text=f"{alumno.nombre} | {alumno.cantidad_cursos} curso(s) | "
                 f"Promedio general: {alumno.promedio_general:.2f}"
        )

    def _registro_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un registro de la tabla.")
            return None
        return self._registro_por_iid[seleccion[0]]

    def editar_seleccionado(self):
        registro = self._registro_seleccionado()
        if registro is not None:
            DialogoEdicion(self, self.gestor, registro, al_guardar=self._refrescar)

    def eliminar_seleccionado(self):
        registro = self._registro_seleccionado()
        if registro is None:
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar el curso '{registro.curso}' de {registro.alumno.nombre}?"):
            self.gestor.eliminar(registro)
            self._refrescar()


def main():
    AppNotas(GestorNotas(RepositorioCSV())).mainloop()


if __name__ == "__main__":
    main()
