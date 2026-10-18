import tkinter as tk
from tkinter import messagebox

from logica import calcular_promedio, determinar_estado
from validaciones import validar_texto_obligatorio, validar_nota
from reportes import construir_reporte
from almacenamiento import guardar_alumnos, cargar_alumnos

lista_alumnos = cargar_alumnos()


def mostrar_reporte(texto):
    txt_resultado.delete("1.0", tk.END)
    txt_resultado.insert(tk.END, texto)


def procesar_datos():
    user = entry_user.get()
    curso = entry_curso.get()

    if not validar_texto_obligatorio(user):
        messagebox.showerror("Error", "El campo 'Nombre' no puede estar vacío.")
        return
    if not validar_texto_obligatorio(curso):
        messagebox.showerror("Error", "El campo 'Curso' no puede estar vacío.")
        return

    try:
        dni = int(entry_dni.get())
        nota_1 = int(entry_nota1.get())
        nota_2 = int(entry_nota2.get())
        nota_3 = int(entry_nota3.get())
        nota_4 = int(entry_nota4.get())
    except ValueError:
        messagebox.showerror(
            "Error",
            "Por favor, asegúrate de llenar todos los campos.\n"
            "DNI y Notas deben ser números enteros."
        )
        return

    for nota in (nota_1, nota_2, nota_3, nota_4):
        if not validar_nota(nota):
            messagebox.showerror("Error", "Las notas deben estar entre 0 y 20.")
            return

    promedio = calcular_promedio(nota_1, nota_2, nota_3, nota_4)
    estado = determinar_estado(promedio)

    alumno = {
        "dni": dni,
        "user": user,
        "curso": curso,
        "notas": [nota_1, nota_2, nota_3, nota_4],
        "promedio": promedio,
        "estado": estado,
    }
    lista_alumnos.append(alumno)
    guardar_alumnos(lista_alumnos)

    texto_salida = construir_reporte(
        user, dni, curso, nota_1, nota_2, nota_3, nota_4, promedio, estado
    )
    mostrar_reporte(texto_salida)


ventana = tk.Tk()
ventana.title("Promediado de Notas")
ventana.geometry("400x600")

tk.Label(ventana, text="¿Cuál es tu nombre?").pack(pady=2)
entry_user = tk.Entry(ventana)
entry_user.pack(fill="x", padx=20, pady=2)

tk.Label(ventana, text="Por favor coloca tu DNI:").pack(pady=2)
entry_dni = tk.Entry(ventana)
entry_dni.pack(fill="x", padx=20, pady=2)

tk.Label(ventana, text="Coloca el curso correspondiente:").pack(pady=2)
entry_curso = tk.Entry(ventana)
entry_curso.pack(fill="x", padx=20, pady=2)

tk.Label(ventana, text="Coloca la primera nota:").pack(pady=2)
entry_nota1 = tk.Entry(ventana)
entry_nota1.pack(fill="x", padx=20, pady=2)

tk.Label(ventana, text="Coloca la segunda nota:").pack(pady=2)
entry_nota2 = tk.Entry(ventana)
entry_nota2.pack(fill="x", padx=20, pady=2)

tk.Label(ventana, text="Coloca la tercera nota:").pack(pady=2)
entry_nota3 = tk.Entry(ventana)
entry_nota3.pack(fill="x", padx=20, pady=2)

tk.Label(ventana, text="Coloca la cuarta nota:").pack(pady=2)
entry_nota4 = tk.Entry(ventana)
entry_nota4.pack(fill="x", padx=20, pady=2)

btn_procesar = tk.Button(ventana, text="Procesar y Mostrar Reporte", command=procesar_datos)
btn_procesar.pack(pady=10)

txt_resultado = tk.Text(ventana, height=13, font=("Courier", 10))
txt_resultado.pack(fill="both", padx=20, pady=5)

ventana.mainloop()