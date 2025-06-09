import time
from buscador import buscar_en_duckduckgo
from lector import extraer_texto_de_url
from analizador import preprocesar
from normalizador import cargar_terminos, normalizar_palabra, guardar_diccionario

# Lista base de temas por estudiar
temas = [
    "física cuántica",
    "mecánica cuántica",
    "principio de incertidumbre",
    "relatividad general",
    "relatividad especial",
    "teoría de cuerdas",
    "química orgánica",
    "química cuántica",
    "entropía",
    "física de partículas"
]

# Diccionario de términos científicos
terminos = cargar_terminos()

def estudiar_tema(tema):
    print(f"\n🧠 Estudiando: {tema}")
    links = buscar_en_duckduckgo(tema)
    for link in links:
        print(f"🔗 Leyendo: {link}")
        try:
            texto = extraer_texto_de_url(link)
            palabras = preprocesar(texto)
            for palabra in palabras:
                normalizar_palabra(palabra, terminos)
            time.sleep(5)  # evitar sobrecargar la red
        except Exception as e:
            print(f"⚠️ Error con {link}: {e}")

    guardar_diccionario(terminos)

if __name__ == '__main__':
    for tema in temas:
        estudiar_tema(tema)
        print("🛌 Descanso breve para simular comportamiento humano...")
        time.sleep(10)