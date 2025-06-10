import numpy as np
import torch
import torch.nn as nn
import re
from normalizador import cargar_terminos, normalizar_palabra

# Cargar términos del normalizador
términos = cargar_terminos()

# Red neuronal simple con PyTorch
class MiniRedTorch(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(MiniRedTorch, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.sigmoid(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x

# Instancia de la red neuronal
modelo = MiniRedTorch(5, 4, 1)

# Función de preprocesamiento
def preprocesar(texto):
    texto = texto.lower()
    texto = re.sub(r'[^\w\s\\\+\-\=\{\}\<\>\.\,\/\:\^\%\°]', '', texto)
    palabras = texto.split()
    palabras_norm = [normalizar_palabra(p, términos) for p in palabras]
    return palabras_norm

# Extraer características desde texto
def extraer_caracteristicas(palabras):
    claves = ['investigación', 'descubrimiento', 'hecho', 'dato', 'ciencia']
    raices = ['investig', 'cient', 'descubr', 'tecnolog', 'anal']

    total_palabras = len(palabras)
    claves_count = sum(1 for p in palabras if p in claves)
    raices_count = sum(1 for p in palabras for r in raices if r in p)
    num_largas = sum(1 for p in palabras if len(p) > 7)
    num_numeros = sum(1 for p in palabras if p.isdigit())

    return [[claves_count, raices_count, num_largas, num_numeros, total_palabras]]


# Método usando red neuronal con PyTorch
def analizar_con_red(texto):
    palabras = preprocesar(texto)
    caracteristicas = extraer_caracteristicas(palabras)[0]
    entrada = torch.tensor(caracteristicas, dtype=torch.float32)
    salida = modelo(entrada)
    resultado = "Informativo" if salida.item() > 0.5 else "Irrelevante"
    return resultado

# Función final que se llama desde main.py
def analizar_con_pregunta(texto, pregunta):
    resultado = analizar_con_red(texto)
    return f"Pregunta: {pregunta}\nRespuesta: {resultado}"