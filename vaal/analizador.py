import numpy as np

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

def analizar(texto):
    x = vectorizar(texto)
    resultado = modelo.predict(x)
    return "Informativo" if resultado[0][0] == 1 else "Irrelevante"