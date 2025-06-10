import json
import urllib.parse
import urllib.request
from html.parser import HTMLParser

# === Manejo del diccionario ===

def cargar_terminos(ruta='diccivaal.json'):
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def guardar_diccionario(diccionario, ruta='diccivaal.json'):
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(diccionario, f, indent=2, ensure_ascii=False)

# === Extracción de texto desde HTML (para DuckDuckGo) ===

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data.strip())

    def get_text(self):
        return ' '.join([t for t in self.text if t])

# === Búsqueda del significado desde DuckDuckGo ===

def buscar_en_duckduckgo(palabra):
    query = urllib.parse.quote(f"{palabra} significado site:wikipedia.org OR site:sciencedirect.com OR site:nature.com")
    url = f"https://html.duckduckgo.com/html/?q={query}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            parser = TextExtractor()
            parser.feed(html)
            return parser.get_text()[:500]
    except Exception as e:
        print(f"[ERROR] No se pudo buscar '{palabra}': {e}")
        return None

# === Validación de palabra antes de intentar definir ===

def es_palabra_valida(palabra):
    if len(palabra) > 30:
        return False
    if all(not c.isalpha() for c in palabra):
        return False
    num_simbolos = sum(1 for c in palabra if not c.isalnum())
    if len(palabra) == 0 or (num_simbolos / len(palabra)) > 0.6:
        return False
    return True

# === Normalización con contexto ===

def normalizar_palabra(palabra, diccionario, contexto="general", verbose=True):
    palabra_lower = palabra.lower().strip()

    if not es_palabra_valida(palabra_lower):
        return palabra_lower

    # Ya está registrada
    if palabra_lower in diccionario:
        entrada = diccionario[palabra_lower]

        # Si tiene múltiples contextos
        if isinstance(entrada, dict) and "contexto" in entrada:
            if contexto in entrada["contexto"]:
                return palabra_lower  # Ya conocido en este contexto
        elif isinstance(entrada, dict) and contexto == "general":
            return palabra_lower  # Ya conocido sin contexto

    # Buscar definición en línea
    definicion = buscar_en_duckduckgo(palabra_lower)
    if definicion:
        if verbose:
            print(f"Nuevo término aprendido: '{palabra_lower}' en contexto '{contexto}'")

        if palabra_lower not in diccionario:
            diccionario[palabra_lower] = {"contexto": {}}

        if "contexto" not in diccionario[palabra_lower]:
            diccionario[palabra_lower]["contexto"] = {}

        diccionario[palabra_lower]["contexto"][contexto] = {
            "definicion": definicion.strip(),
            "sinonimos": []
        }

        guardar_diccionario(diccionario)
        return palabra_lower

    # Si no encontró nada
    return palabra_lower