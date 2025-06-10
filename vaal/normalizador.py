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