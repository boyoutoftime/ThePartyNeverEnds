import fasttext
import os

modelos_fasttext = {}
modelo_detector_idioma = None

def cargar_detector_idioma(ruta='lid.176.bin'):
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
        'es': 'cc.es.300.bin',
        'en': 'cc.en.300.bin',
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