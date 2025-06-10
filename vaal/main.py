# main.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from analizador import resumir_textos, analizar_con_pregunta

app = FastAPI()

# Modelo para recibir datos JSON
class Peticion(BaseModel):
    texto: str
    pregunta: str = None  # Opcional

@app.get("/")
def raiz():
    return {"mensaje": "🧠 IA Investigadora activa"}

@app.post("/analizar")
def analizar(peticion: Peticion):
    texto = peticion.texto
    pregunta = peticion.pregunta

    if pregunta:
        respuesta = analizar_con_pregunta(texto, pregunta)
        return {"respuesta": respuesta}
    else:
        resumen = resumir_textos([texto])
        return {"resumen": resumen}
