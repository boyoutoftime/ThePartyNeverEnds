from fastapi import FastAPI
from app.buscador import buscar_en_duckduckgo
from app.lector import extraer_texto_de_url
from app.analizador import resumir_textos
from app.personalidad import dar_estilo

app = FastAPI()

@app.get("/investigar")
def investigar(tema: str):
    links = buscar_en_duckduckgo(tema)
    textos = [extraer_texto_de_url(link) for link in links]
    resumen = resumir_textos(textos)
    respuesta_final = dar_estilo(resumen, tono="profesional", firma=True)
    return {
        "tema": tema,
        "respuesta": respuesta_final
    }