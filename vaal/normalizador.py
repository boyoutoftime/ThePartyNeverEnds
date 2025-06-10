import fasttext
import os

# Cargar modelo fastText solo una vez
modelo_ft = None
def cargar_fasttext(ruta='cc.es.300.bin'):
    global modelo_ft
    if modelo_ft is None and os.path.exists(ruta):
        print("→ Cargando modelo fastText...")
        modelo_ft = fasttext.load_model(ruta)
    return modelo_ft

def normalizar_palabra(palabra, diccionario, contexto="general", verbose=True):
    palabra_lower = palabra.lower().strip()
    if not es_palabra_valida(palabra_lower):
        return palabra_lower

    # Cargar fastText
    ft = cargar_fasttext()

    # Verificar si fastText la conoce
    if ft is not None:
        vector = ft.get_word_vector(palabra_lower)
        if vector.any():  # Tiene representación, palabra válida
            if verbose:
                print(f"[fastText] Palabra reconocida: '{palabra_lower}'")
            return palabra_lower

    # Verificar si ya la conocíamos
    if palabra_lower in diccionario:
        entrada = diccionario[palabra_lower]
        if isinstance(entrada, dict) and "contexto" in entrada:
            if contexto in entrada["contexto"]:
                return palabra_lower
        elif isinstance(entrada, dict) and contexto == "general":
            return palabra_lower

    # Si no existe en fastText ni en el diccionario → buscar en línea
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