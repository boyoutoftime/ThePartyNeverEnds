import random
import re
from normalizador import cargar_terminos, normalizar_palabra

términos = cargar_terminos()

# Red neuronal simple sin numpy
class MiniRedNeuronal:
    def __init__(self, input_size, hidden_size, output_size):
        self.w1 = [[random.uniform(-1, 1) for _ in range(hidden_size)] for _ in range(input_size)]
        self.b1 = [0.0 for _ in range(hidden_size)]
        self.w2 = [[random.uniform(-1, 1) for _ in range(output_size)] for _ in range(hidden_size)]
        self.b2 = [0.0 for _ in range(output_size)]

    def sigmoid(self, x):
        return 1 / (1 + pow(2.718281828, -x))

    def dot(self, v1, v2):
        return sum(a * b for a, b in zip(v1, v2))

    def forward(self, x):
        z1 = [self.dot(x, col) + b for col, b in zip(zip(*self.w1), self.b1)]
        a1 = [self.sigmoid(z) for z in z1]
        z2 = [self.dot(a1, col) + b for col, b in zip(zip(*self.w2), self.b2)]
        output = [self.sigmoid(z) for z in z2]
        return output

    def predict(self, x):
        output = self.forward(x)
        return [1 if o > 0.5 else 0 for o in output]

# Red neuronal para entrada de 5 características
modelo = MiniRedNeuronal(5, 4, 1)


def preprocesar(texto):
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