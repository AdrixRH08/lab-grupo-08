import tkinter as tk
from tkinter import messagebox

# =========================================================
# PASO 2: Funciones CON retorno (hacen un cálculo y devuelven un valor)
# =========================================================

def calcular_promedio(n1, n2, n3, n4):
    """Recibe 4 notas y RETORNA el promedio (float)."""
    return (n1 + n2 + n3 + n4) / 4


def determinar_estado(promedio):
    """Recibe un promedio y RETORNA el texto de estado."""
    if promedio < 11:
        return "DESAPROBADO"
    elif promedio <= 20:
        return "APROBADO"
    else:
        return "INVÁLIDO"


def construir_reporte(user, dni, curso, n1, n2, n3, n4, promedio, estado):
    """Recibe todos los datos y RETORNA el texto final ya formateado."""
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


# =========================================================
# PASO 2: Funciones SIN retorno (solo producen un efecto: mostrar algo)
# =========================================================

def mostrar_reporte(texto):
    """No retorna nada. Solo escribe el texto en el widget de resultado."""
    txt_resultado.delete("1.0", tk.END)
    txt_resultado.insert(tk.END, texto)


def mostrar_menu():
    """Ejemplo de función sin retorno, solo imprime información en consola."""
    print("1. Registrar notas")
    print("2. Consultar resultado")


# =========================================================
# PASO 3: Paso de parámetros por VALOR y por REFERENCIA
# =========================================================

def intentar_modificar_valor(x):
    """
    x es un int (tipo INMUTABLE en Python).
    Sumarle algo aquí NO modifica la variable original que se pasó
    desde fuera; se comporta como "paso por valor".
    """
    x = x + 10
    return x


def agregar_nota_extra(lista_notas):
    """
    lista_notas es una LISTA (tipo MUTABLE en Python).
    Modificarla aquí (append) SÍ afecta la lista original
    que existe fuera de la función; se comporta como "paso por referencia".
    """
    lista_notas.append(0)


def demostrar_valor_y_referencia():
    """
    Función de evidencia para el Paso 3: compara el valor antes y
    después de llamar a las dos funciones anteriores, e imprime
    el resultado en consola (para captura de pantalla).
    """
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


# =========================================================
# PASO 4: Alcance de variables (scope)
# =========================================================
# Las variables entry_user, entry_dni, etc. y txt_resultado son GLOBALES
# porque pertenecen a la interfaz gráfica (el programa principal) y deben
# ser accesibles desde cualquier función que dibuje o lea la ventana.
#
# En cambio, dentro de calcular_promedio(), determinar_estado(),
# construir_reporte(), etc. las variables (n1, n2, promedio, estado...)
# son LOCALES: existen solo mientras la función se ejecuta y desaparecen
# al terminar. No dependen de ninguna variable global con el mismo nombre.

def procesar_datos():
    """
    Función 'orquestadora': se conecta con la GUI (variables globales
    de los widgets), pero delega el cálculo y el armado del texto a
    funciones con retorno, y delega el mostrar resultado a una función
    sin retorno. Aquí también se ejecuta la demostración del Paso 3.
    """
    # 1. ENTRADA: se leen los valores desde las cajas de texto (widgets globales)
    user = entry_user.get()

    try:
        dni = int(entry_dni.get())
        curso = entry_curso.get()
        nota_1 = int(entry_nota1.get())
        nota_2 = int(entry_nota2.get())
        nota_3 = int(entry_nota3.get())
        nota_4 = int(entry_nota4.get())

        # Restricción básica (Paso 1): las notas deben estar en el rango 0-20
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

    # 2. PROCESO: todas estas variables (promedio, estado) son LOCALES a esta función
    promedio = calcular_promedio(nota_1, nota_2, nota_3, nota_4)
    estado = determinar_estado(promedio)

    # Evidencia del Paso 3 (se ve en la consola donde corre el script)
    demostrar_valor_y_referencia()

    # 3. SALIDA
    texto_salida = construir_reporte(
        user, dni, curso, nota_1, nota_2, nota_3, nota_4, promedio, estado
    )
    mostrar_reporte(texto_salida)


# =========================================================
# CONFIGURACIÓN DE LA VENTANA (programa principal)
# =========================================================
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

# Llamada de ejemplo a la función sin retorno mostrar_menu() (Paso 2),
# se ve en consola al iniciar el programa
mostrar_menu()

ventana.mainloop()