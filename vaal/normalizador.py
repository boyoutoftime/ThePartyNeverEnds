import fasttext
import os

# --- Código fastText para detección y carga de modelos ---

modelos_fasttext = {}
modelo_detector_idioma = None

def cargar_detector_idioma(ruta='~/fasttext/lid.176.bin'):
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
        return "es"  # fallback a español
    etiquetas, _ = modelo.predict(texto)
    etiqueta = etiquetas[0]  # Ejemplo: '__label__es'
    idioma = etiqueta.replace("__label__", "")
    return idioma

def cargar_fasttext_por_idioma(idioma):
    rutas = {
        'es': '~/fasttext/cc.es.300.bin',
        'en': '~/fasttext/cc.en.300.bin',
        # Agrega más idiomas si quieres
    }

    if idioma not in modelos_fasttext:
        ruta = rutas.get(idioma)
        if ruta and os.path.exists(ruta):
            print(f"→ Cargando fastText para idioma '{idioma}'")
            modelos_fasttext[idioma] = fasttext.load_model(ruta)
        else:
            print(f"[ADVERTENCIA] No se encontró modelo para idioma '{idioma}'")
            modelos_fasttext[idioma] = None

    return modelos_fasttext[idioma]

def es_palabra_valida(palabra):
    # Implementa aquí la validación que usas para palabras válidas
    # Ejemplo simple:
    return palabra.isalpha()

def normalizar_palabra(palabra, diccionario, contexto="general", verbose=True):
    palabra_lower = palabra.lower().strip()
    if not es_palabra_valida(palabra_lower):
        return palabra_lower

    # Detectar idioma con fastText
    idioma = detectar_idioma_fasttext(palabra_lower)
    if verbose:
        print(f"[Detector fastText] Idioma detectado: {idioma}")

    # Cargar modelo fastText para ese idioma
    ft = cargar_fasttext_por_idioma(idioma)

    # Verificar si fastText reconoce la palabra
    if ft is not None:
        vector = ft.get_word_vector(palabra_lower)
        if vector.any():
            if verbose:
                print(f"[fastText-{idioma}] Palabra reconocida: '{palabra_lower}'")
            return palabra_lower

    # Revisar si ya está en el diccionario
    if palabra_lower in diccionario:
        entrada = diccionario[palabra_lower]
        if isinstance(entrada, dict) and "contexto" in entrada:
            if contexto in entrada["contexto"]:
                return palabra_lower
        elif isinstance(entrada, dict) and contexto == "general":
            return palabra_lower

    # Si no se reconoce y no quieres buscar online, solo devuelves palabra_lower aquí
    return palabra_lower

# --- Función para normalizar texto completo ---

def normalizar_texto(texto, diccionario, contexto="general", verbose=False):
    palabras = texto.split()
    normalizadas = []

    for palabra in palabras:
        palabra_limpia = normalizar_palabra(palabra, diccionario, contexto, verbose=verbose)
        normalizadas.append(palabra_limpia)

    return " ".join(normalizadas)

# --- Aquí debería ir tu función detectar_bloques_latex, que retorna texto unido y lista de ecuaciones ---

# Por ejemplo (simplificado):
def detectar_bloques_latex(texto):
    # Aquí va tu código real que ya tienes y que separa texto y ecuaciones LaTeX
    # Para este ejemplo retorno fijo:
    texto_unido = "Este es un documento sobre física cuántica. La ecuación de Schrödinger es: También existen expresiones como y otras fórmulas. Este texto debe ir como bloque normal."
    ecuaciones = [
        "$i\\hbar\\frac{\\partial}{\\partial t}\\Psi = \\hat{H}\\Psi$",
        "$E = mc^2$"
    ]
    return texto_unido, ecuaciones

# --- Flujo principal ---

if __name__ == "__main__":
    texto_original = """
    Este es un documento sobre física cuántica.
    La ecuación de Schrödinger es: $i\\hbar\\frac{\\partial}{\\partial t}\\Psi = \\hat{H}\\Psi$
    También existen expresiones como $E = mc^2$ y otras fórmulas.
    Este texto debe ir como bloque normal.
    """

    diccionario = {}  # Tu diccionario semántico si tienes

    texto_unido, ecuaciones = detectar_bloques_latex(texto_original)

    texto_normalizado = normalizar_texto(texto_unido, diccionario, contexto="física", verbose=True)

    print("\n→ TEXTO NORMALIZADO:")
    print(texto_normalizado)

    print("\n→ ECUACIONES (sin tocar):")
    for eq in ecuaciones:
        print("-", eq)