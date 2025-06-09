import json

def cargar_terminos(ruta='terminos_cientificos.json'):
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def normalizar_palabra(palabra, diccionario):
    for clave, sinonimos in diccionario.items():
        if palabra.lower() == clave.lower() or palabra.lower() in [s.lower() for s in sinonimos]:
            return clave
    return palabra

import urllib.parse
import urllib.request
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data.strip())

    def get_text(self):
        return ' '.join([t for t in self.text if t])