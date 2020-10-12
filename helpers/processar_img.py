import random


def processar_img(path=""):
    list_estados = ("vazio", "normal", "cheio")
    estado = random.choice(list_estados)
    return estado
