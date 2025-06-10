import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import random
import re
from normalizador import cargar_terminos, normalizar_palabra

términos = cargar_terminos()

# class MiniRedTorch(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(MiniRedTorch, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.sigmoid(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x
    
    def analizar(texto):
        palabras = preprocesar(texto)
        caracteristicas = extraer_caracteristicas(palabras)[0]
        entrada = torch.tensor(caracteristicas, dtype=torch.float32)

    salida = modelo(entrada)
    resultado = "Informativo" if salida.item() > 0.5 else "Irrelevante"
    return resultado

   
    salida = modelo(entrada)
    resultado = "Informativo" if salida.item() > 0.5 else "Irrelevante"
    return resultado

# Red neuronal para entrada de 5 características
modelo = MiniRedTorch(5, 4, 1)


def preprocesar(texto, terminos):
    texto = texto.lower()
    texto = re.sub(r'[^\w\s\\\+\-\=\{\}\<\>\.\,\/\:\^\%\°]', '', texto)
    palabras = texto.split()
    palabras_norm = [normalizar_palabra(p, terminos) for p in palabras]
    return palabras


def extraer_caracteristicas(palabras):
    claves = ['investigación', 'descubrimiento', 'hecho', 'dato', 'ciencia']
    raices = ['investig', 'cient', 'descubr', 'tecnolog', 'anal']

    total_palabras = len(palabras)
    claves_count = sum(1 for p in palabras if p in claves)
    raices_count = sum(1 for p in palabras for r in raices if r in p)
    num_largas = sum(1 for p in palabras if len(p) > 7)
    num_numeros = sum(1 for p in palabras if p.isdigit())

    return [[claves_count, raices_count, num_largas, num_numeros, total_palabras]]


def analisis_contextual(caracteristicas):
    claves, raices, largas, numeros, total = caracteristicas[0]

    if claves >= 2 and raices >= 1:
        return "Informativo"
    elif total < 5 and claves == 0:
        return "Irrelevante"
    elif numeros > 2:
        return "Probablemente datos"
    else:
        return "Indeterminado"


def analizar(texto):
    palabras = preprocesar(texto)
    caracteristicas = extraer_caracteristicas(palabras)
    resultado = analisis_contextual(caracteristicas)
    return resultado

def analizar_con_pregunta(texto, pregunta):
    # Usa la función principal 'analizar' para aplicar análisis general
    resultado = analizar(texto)
    return f"Pregunta: {pregunta}\nRespuesta: {resultado}"