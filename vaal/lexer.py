import fitz  # PyMuPDF
import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Regex para detectar patrones LaTeX básicos y símbolos matemáticos comunes
ECUACION_REGEX = re.compile(
    r'(\$.*?\$|\\.*?\\|\\.*?\\|\\begin\{equation\}.*?\\end\{equation\}|[∑∫√≈≠≤≥∞∂])',
    re.DOTALL
)

# Cargar modelo MathBERT finetuneado para clasificación
# Nota: reemplaza con el modelo que descargaste o uno que hayas entrenado
MODEL_NAME = "tbs17/mathbert"  # o ruta local a tu modelo
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

def extraer_texto_pdf(ruta_pdf):
    texto_total = ""
    with fitz.open(ruta_pdf) as doc:
        for pagina in doc:
            texto_total += pagina.get_text()
    return texto_total

def es_ecuacion_regex(texto):
    return bool(ECUACION_REGEX.search(texto))

def clasificar_mathbert(texto):
    inputs = tokenizer(texto, return_tensors="pt", truncation=True, max_length=512)
    outputs = model(**inputs)
    logits = outputs.logits
    # Supongamos que clase 1 es "matemáticas", clase 0 es "texto normal"
    pred = torch.argmax(logits, dim=1).item()
    return pred == 1

def lexer(texto):
    # Divide texto en párrafos o líneas
    fragmentos = [frag.strip() for frag in texto.split('\n') if frag.strip()]
    texto_limpio = []
    ecuaciones = []

    for frag in fragmentos:
        # Detección preliminar por regex
        if es_ecuacion_regex(frag):
            # Confirmación por MathBERT
            if clasificar_mathbert(frag):
                ecuaciones.append(frag)
            else:
                texto_limpio.append(frag)
        else:
            texto_limpio.append(frag)

    return texto_limpio, ecuaciones

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python lexer.py archivo.pdf")
        sys.exit(1)

    archivo_pdf = sys.argv[1]
    texto = extraer_texto_pdf(archivo_pdf)
    if not texto.strip():
        print("⚠️ El PDF no contiene texto o no se pudo extraer.")
        sys.exit(1)

    texto_limpio, ecuaciones = lexer(texto)

    print("\n=== TEXTO DETECTADO (limpio) ===\n")
    for t in texto_limpio:
        print(t)

    print("\n=== ECUACIONES DETECTADAS ===\n")
    for i, eq in enumerate(ecuaciones):
        print(f"[{i+1}] {eq}")