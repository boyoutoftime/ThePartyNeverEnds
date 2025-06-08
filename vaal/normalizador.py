import json

with open('terminos_cientificos.json', 'r', encoding='utf-8') as f:
    terminos = json.load(f)

def normalizar_texto(texto):
    for termino, sinonimos in terminos.items():
        for sinonimo in sinonimos:
            texto = texto.replace(sinonimo.lower(), termino.lower())
    return texto