import os
import fasttext
from bpemb import BPEmb
import re

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
        return "es"  # Fallback
    etiquetas, _ = modelo.predict(texto)
    etiqueta = etiquetas[0]
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

# --- VALIDACIÓN Y NORMALIZACIÓN --- #

def es_palabra_valida(palabra):
    return palabra.isalpha()

def normalizar_palabra(palabra, diccionario, contexto="general", verbose=True):
    palabra_lower = palabra.lower().strip()
    if not es_palabra_valida(palabra_lower):
        return palabra_lower

    idioma = detectar_idioma_fasttext(palabra_lower)
    if verbose:
        print(f"[Detector fastText] Idioma detectado: {idioma}")

    bpemb = cargar_bpemb(idioma)
    if bpemb is not None:
        tokens = bpemb.encode(palabra_lower)
        if tokens:
            if verbose:
                print(f"[BPEmb-{idioma}] Palabra reconocida: '{palabra_lower}' → tokens: {tokens}")
            return palabra_lower

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

# --- DETECCIÓN Y MARCADO DE BLOQUES LaTeX --- #

def detectar_bloques_latex(texto):
    patron = r"(\$.*?\$)"  # Detecta bloques LaTeX simples en una línea
    ecuaciones = re.findall(patron, texto)

    texto_con_marcas = texto
    for i, eq in enumerate(ecuaciones):
        marcador = f"<<EQ{i}>>"
        texto_con_marcas = texto_con_marcas.replace(eq, marcador, 1)

    return texto_con_marcas, ecuaciones

# --- REINSERCIÓN DE ECUACIONES --- #

def reinsertar_ecuaciones(texto_con_marcas, ecuaciones):
    for i, eq in enumerate(ecuaciones):
        marcador = f"<<EQ{i}>>"
        texto_con_marcas = texto_con_marcas.replace(marcador, eq)
    return texto_con_marcas

# --- FLUJO PRINCIPAL --- #

if __name__ == "__main__":
    texto_original = """
    Este es un documento sobre física cuántica.
    La ecuación de Schrödinger es: $i\\hbar\\frac{\\partial}{\\partial t}\\Psi = \\hat{H}\\Psi$
    También existen expresiones como $E = mc^2$ y otras fórmulas.
    Este texto debe ir como bloque normal.
    """

    diccionario = {}  # Diccionario semántico personalizado

    # 1. Detectar ecuaciones y marcar con <<EQi>>
    texto_marcado, ecuaciones = detectar_bloques_latex(texto_original)

    # 2. Normalizar solo el texto
    texto_normalizado = normalizar_texto(texto_marcado, diccionario, contexto="física", verbose=True)

    # 3. Reinsertar ecuaciones donde estaban
    texto_final = reinsertar_ecuaciones(texto_normalizado, ecuaciones)

    print("\n→ TEXTO FINAL NORMALIZADO + REINSERTADO:")
    print(texto_final)

    print("\n→ ECUACIONES:")
    for eq in ecuaciones:
        print("-", eq)