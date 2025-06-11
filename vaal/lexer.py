import fitz  # PyMuPDF
import sys
from pylatexenc.latexwalker import LatexWalker, LatexCharsNode, LatexMathNode

def detectar_bloques_latex(texto):
    try:
        walker = LatexWalker(texto)
        nodelist, *_ = walker.get_latex_nodes(pos=0)
    except Exception as e:
        print(f"[ERROR en el análisis LaTeX]: {e}")
        return "", []

    texto_normal = []
    ecuaciones = []

    for nodo in nodelist:
        if isinstance(nodo, LatexCharsNode):
            fragmento = nodo.chars.strip()
            if fragmento:
                texto_normal.append(fragmento)

        elif isinstance(nodo, LatexMathNode):
            contenido = nodo.latex_verbatim().strip()
            ecuaciones.append(contenido)

    texto_unido = " ".join(texto_normal).strip()
    return texto_unido, ecuaciones

def extraer_texto_pdf(ruta_pdf):
    try:
        texto_total = ""
        with fitz.open(ruta_pdf) as doc:
            for pagina in doc:
                texto_total += pagina.get_text()
        return texto_total
    except Exception as e:
        print(f"[ERROR al leer el PDF]: {e}")
        return ""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python analizar_pdf_latex.py archivo.pdf")
        sys.exit(1)

    archivo_pdf = sys.argv[1]
    texto = extraer_texto_pdf(archivo_pdf)

    if not texto.strip():
        print("⚠️ El PDF no contiene texto o no se pudo extraer.")
        sys.exit(1)

    texto_normal, ecuaciones = detectar_bloques_latex(texto)

    print("\n=== TEXTO DETECTADO (limpio) ===\n")
    
    print("\n=== ECUACIONES DETECTADAS ===\n")
    for i, eq in enumerate(ecuaciones):
        print(f"[{i+1}] {eq}")