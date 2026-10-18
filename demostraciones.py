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


if __name__ == "__main__":
    mostrar_menu()
    demostrar_valor_y_referencia()