import json
import urllib.parse
import urllib.request
from html.parser import HTMLParser

def cargar_terminos(ruta='diccivaal.json'):
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_diccionario(diccionario, ruta='diccivaal.json'):
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(diccionario, f, indent=2, ensure_ascii=False)

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

def es_palabra_valida(palabra):
    if len(palabra) > 30:
        return False
    if all(not c.isalpha() for c in palabra):
        return False
    num_simbolos = sum(1 for c in palabra if not c.isalnum())
    if num_simbolos / len(palabra) > 0.6:
        return False
    return True

def normalizar_palabra(palabra, diccionario):
    palabra_lower = palabra.lower()

    if not es_palabra_valida(palabra_lower):
        return palabra  # Ignorar palabras no válidas

    for clave, sinonimos in diccionario.items():
        if palabra_lower == clave.lower() or palabra_lower in [s.lower() for s in sinonimos]:
            return clave

    definicion = buscar_en_duckduckgo(palabra)
    if definicion:
        print(f"Nuevo término aprendido: {palabra} → {definicion[:60]}...")
        diccionario[palabra] = []
        guardar_diccionario(diccionario)
        return palabra

    return palabra

    definicion = buscar_en_duckduckgo(palabra)
    if definicion:
        print(f"Nuevo término aprendido: {palabra} → {definicion[:60]}...")
        diccionario[palabra] = []
        guardar_diccionario(diccionario)
        return palabra

    return palabra