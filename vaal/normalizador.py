from langdetect import detect
import fasttext
import os

modelos_fasttext = {}

def cargar_fasttext_por_idioma(idioma):
    rutas = {
        'es': 'cc.es.300.bin',
        'en': 'cc.en.300.bin',
        # Agrega aquí más idiomas si los descargas
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

    # Detectar idioma
    try:
        idioma = detect(palabra_lower)
    except:
        idioma = "es"  # por defecto español si falla

    # Cargar fastText del idioma detectado
    ft = cargar_fasttext_por_idioma(idioma)

    # Verificar si fastText la reconoce
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

    # Buscar online si no se reconoce
    definicion = buscar_en_duckduckgo(palabra_lower)
    if definicion:
        if verbose:
            print(f"[DuckDuckGo] Nuevo término: '{palabra_lower}' en contexto '{contexto}'")

        if palabra_lower not in diccionario:
            diccionario[palabra_lower] = {"contexto": {}}
        diccionario[palabra_lower]["contexto"][contexto] = {
            "definicion": definicion.strip(),
            "sinonimos": []
        }
        guardar_diccionario(diccionario)
        return palabra_lower

    return palabra_lower