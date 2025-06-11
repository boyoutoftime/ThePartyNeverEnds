import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import chardet

def leer_archivo_con_detec_encoding(ruta_archivo, default="utf-8"):
    with open(ruta_archivo, "rb") as f:
        rawdata = f.read()
    resultado = chardet.detect(rawdata)
    encoding = resultado.get('encoding')

    if not encoding:
        print(f"[WARN] Codificación no detectada. Usando por defecto: {default}")
        encoding = default
    else:
        print(f"[INFO] Codificación detectada: {encoding}")

    try:
        texto = rawdata.decode(encoding, errors="ignore")
    except Exception as e:
        print(f"[ERROR al decodificar con {encoding}]: {e}")
        texto = rawdata.decode(default, errors="ignore")

    return texto

class MathBertLexer:
    def __init__(self, model_name="tbs17/mathbert"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.eval()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def clasificar_fragmento(self, texto):
        inputs = self.tokenizer(texto, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=1)
            pred = torch.argmax(probs, dim=1).item()
            return pred, probs[0][pred].item()

    def procesar_texto(self, texto, separador="\n\n"):
        fragmentos = texto.split(separador)
        texto_normal = []
        fragmentos_matematicos = []

        for fragmento in fragmentos:
            fragmento = fragmento.strip()
            if not fragmento:
                continue
            etiqueta, confianza = self.clasificar_fragmento(fragmento)
            if etiqueta == 1:
                fragmentos_matematicos.append(fragmento)
            else:
                texto_normal.append(fragmento)

        return texto_normal, fragmentos_matematicos

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python lexer.py archivo.txt")
        sys.exit(1)

    archivo = sys.argv[1]
    texto = leer_archivo_con_detec_encoding(archivo)

    lexer = MathBertLexer()
    texto_normal, fragmentos_matematicos = lexer.procesar_texto(texto)

    print("=== TEXTO NORMAL ===")
    for t in texto_normal:
        print(t)
        print("---")

    print("\n=== FRAGMENTOS MATEMÁTICOS ===")
    for f in fragmentos_matematicos:
        print(f)
        print("---")