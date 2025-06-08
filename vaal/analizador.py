import numpy as np
import re
from normalizador import cargar_texto, normalizar_palabra

términos = cargar_terminos()

# Red neuronal muy simple para clasificar frases como "informativa" o "irrelevante"
class MiniRedNeuronal:
    def __init__(self, input_size, hidden_size, output_size):
        self.w1 = np.random.randn(input_size, hidden_size)
        self.b1 = np.zeros((1, hidden_size))
        self.w2 = np.random.randn(hidden_size, output_size)
        self.b2 = np.zeros((1, output_size))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def forward(self, x):
        self.z1 = x @ self.w1 + self.b1
        self.a1 = self.sigmoid(self.z1)
        self.z2 = self.a1 @ self.w2 + self.b2
        output = self.sigmoid(self.z2)
        return output

    def predict(self, x):
        resultado = self.forward(x)
        return (resultado > 0.5).astype(int)

# Convertimos texto en vectores muy simples (cuenta de palabras clave)
def vectorizar(texto):
    claves = ['investigación', 'descubrimiento', 'hecho', 'dato', 'ciencia']
    vector = np.array([[texto.lower().count(palabra) for palabra in claves]])
    return vector

# Crear la red (input: 5 palabras clave, hidden: 4 neuronas, salida: 1)
modelo = MiniRedNeuronal(5, 4, 1)


def preprocesar(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-záéíóúüñ\s]', '', texto)  # Solo letras y espacios
    texto = normalizar_texto(texto)
    palabras = texto.split()
    palabras_norm = [normalizar_palabra(p, terminos) for p in palabra)
    return palabras


def extraer_caracteristicas(palabras):
    claves = ['investigación', 'descubrimiento', 'hecho', 'dato', 'ciencia']
    raices = ['investig', 'cient', 'descubr', 'tecnolog', 'anal']
    
    total_palabras = len(palabras)
    claves_count = sum(1 for p in palabras if p in claves)
    raices_count = sum(1 for p in palabras for r in raices if r in p)
    num_largas = sum(1 for p in palabras if len(p) > 7)
    num_numeros = sum(1 for p in palabras if p.isdigit())
    
    return np.array([[claves_count, raices_count, num_largas, num_numeros, total_palabras]])


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