lista_alumnos = []
import tkinter as tk
from almacenamiento import guardar_alumnos, cargar_alumnos
from tkinter import messagebox

def calcular_promedio(n1, n2, n3, n4):
    return (n1 + n2 + n3 + n4) / 4


def determinar_estado(promedio):
    if promedio < 11:
        return "DESAPROBADO"
    elif promedio <= 20:
        return "APROBADO"
    else:
        return "INVÁLIDO"

def validar_texto_obligatorio(texto, nombre_campo): 
    if texto is None or texto.strip() == "":
        messagebox.showerror("Error", f"El campo '{nombre_campo}' no puede estar vacío.")
        return False
    return True

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

def mostrar_reporte(texto):
    txt_resultado.delete("1.0", tk.END)
    txt_resultado.insert(tk.END, texto)


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

def procesar_datos():
    user = entry_user.get()
    curso = entry_curso.get()

    if not validar_texto_obligatorio(user, "Nombre"):
        return
    if not validar_texto_obligatorio(curso, "Curso"):
        return

    try:
        dni = int(entry_dni.get())
        curso = entry_curso.get()
        nota_1 = int(entry_nota1.get())
        nota_2 = int(entry_nota2.get())
        nota_3 = int(entry_nota3.get())
        nota_4 = int(entry_nota4.get())

        for nota in (nota_1, nota_2, nota_3, nota_4):
            if nota < 0 or nota > 20:
                messagebox.showerror("Error", "Las notas deben estar entre 0 y 20.")
                return

    except ValueError:
        messagebox.showerror(
            "Error",
            "Por favor, asegúrate de llenar todos los campos.\n"
            "DNI y Notas deben ser números enteros."
        )
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

lista_alumnos = cargar_alumnos()

mostrar_menu()

ventana.mainloop()