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