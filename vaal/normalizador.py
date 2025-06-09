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

def buscar_en_duckduckgo(palabra):
    query = urllib.parse.quote(palabra + " significado site:wikipedia.org OR site:sciencedirect.com OR site:nature.com")
    url = f"https://html.duckduckgo.com/html/?q={query}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            parser = TextExtractor()
            parser.feed(html)
            return parser.get_text()[:500]
    except:
        return None
def guardar_diccionario(diccionario, ruta='terminos_cientificos.json'):
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(diccionario, f, indent=2, ensure_ascii=False)
