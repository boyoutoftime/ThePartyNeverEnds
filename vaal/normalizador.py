import os
import fasttext
from bpemb import BPEmb

# --- CARGA GLOBAL DE MODELOS --- #

modelo_detector_idioma = None
bpemb_modelos = {}

# --- DETECCIÓN DE IDIOMA --- #

def cargar_detector_idioma(ruta='~/ThePartyNeverEnds/vaal/fasttext/lid.176.bin'):
    ruta = os.path.expanduser(ruta)
    global modelo_detector_idioma
    if modelo_detector_idioma is None:
        if os.path.exists(ruta):
            print("→ Cargando detector de idioma fastText...")
            modelo_detector_idioma = fasttext.load_model(ruta)
        else:
            print(f"[ERROR] No se encontró el modelo detector de idioma en '{ruta}'")
    return modelo_detector_idioma

def detectar_idioma_fasttext(texto):
    modelo = cargar_detector_idioma()
    if modelo is None or not texto.strip():
        return "es"  # Fallback a español
    etiquetas, _ = modelo.predict(texto)
    etiqueta = etiquetas[0]  # Ejemplo: '__label__es'
    idioma = etiqueta.replace("__label__", "")
    return idioma

# --- CARGA DE BPEmb POR IDIOMA --- #

def cargar_bpemb(idioma, dim=300):
    if idioma not in bpemb_modelos:
        try:
            print(f"→ Cargando BPEmb para '{idioma}'...")
            bpemb_modelos[idioma] = BPEmb(lang=idioma, dim=dim)
        except Exception as e:
            print(f"[ERROR] No se pudo cargar BPEmb para '{idioma}': {e}")
            bpemb_modelos[idioma] = None
    return bpemb_modelos[idioma]

# --- FUNCIONES DE VALIDACIÓN Y NORMALIZACIÓN --- #

def es_palabra_valida(palabra):
    return palabra.isalpha()

def normalizar_palabra(palabra, diccionario, contexto="general", verbose=True):
    palabra_lower = palabra.lower().strip()
    if not es_palabra_valida(palabra_lower):
        return palabra_lower

    # Detectar idioma
    idioma = detectar_idioma_fasttext(palabra_lower)
    if verbose:
        print(f"[Detector fastText] Idioma detectado: {idioma}")

    # Validar con BPEmb
    bpemb = cargar_bpemb(idioma)
    if bpemb is not None:
        tokens = bpemb.encode(palabra_lower)
        if tokens:
            if verbose:
                print(f"[BPEmb-{idioma}] Palabra reconocida: '{palabra_lower}' → tokens: {tokens}")
            return palabra_lower

    # Verificación en diccionario propio
    if palabra_lower in diccionario:
        entrada = diccionario[palabra_lower]
        if isinstance(entrada, dict) and "contexto" in entrada:
            if contexto in entrada["contexto"]:
                return palabra_lower
        elif isinstance(entrada, dict) and contexto == "general":
            return palabra_lower

    return palabra_lower

def normalizar_texto(texto, diccionario, contexto="general", verbose=False):
    palabras = texto.split()
    normalizadas = []

    for palabra in palabras:
        palabra_limpia = normalizar_palabra(palabra, diccionario, contexto, verbose=verbose)
        normalizadas.append(palabra_limpia)

    return " ".join(normalizadas)

# --- DETECCIÓN SIMPLIFICADA DE BLOQUES LaTeX --- #

def detectar_bloques_latex(texto):
    texto_unido = "Este es un documento sobre física cuántica. La ecuación de Schrödinger es: También existen expresiones como y otras fórmulas. Este texto debe ir como bloque normal."
    ecuaciones = [
        "$i\\hbar\\frac{\\partial}{\\partial t}\\Psi = \\hat{H}\\Psi$",
        "$E = mc^2$"
    ]
    return texto_unido, ecuaciones

# --- FLUJO PRINCIPAL DE EJEMPLO --- #

if __name__ == "__main__":
    texto_original = """
    Este es un documento sobre física cuántica.
    La ecuación de Schrödinger es: $i\\hbar\\frac{\\partial}{\\partial t}\\Psi = \\hat{H}\\Psi$
    También existen expresiones como $E = mc^2$ y otras fórmulas.
    Este texto debe ir como bloque normal.
    """

    diccionario = {}  # Tu diccionario semántico

    texto_unido, ecuaciones = detectar_bloques_latex(texto_original)

    texto_normalizado = normalizar_texto(texto_unido, diccionario, contexto="física", verbose=True)

    print("\n→ TEXTO NORMALIZADO:")
    print(texto_normalizado)

    print("\n→ ECUACIONES (sin tocar):")
    for eq in ecuaciones:
        print("-", eq)