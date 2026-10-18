def validar_texto_obligatorio(texto):
    return texto is not None and texto.strip() != ""


def validar_nota(nota):
    return 0 <= nota <= 20