from pylatexenc.latexwalker import LatexWalker, LatexEnvironmentNode, LatexCharsNode, LatexMathNode
from pylatexenc.latex2text import LatexNodes2Text

def detectar_bloques_latex(texto):
    walker = LatexWalker(texto)
    result = walker.get_latex_nodes(pos=0)
    nodelist = result[0] if isinstance(result, tuple) else result  # Compatibilidad segura

    texto_normal = []
    ecuaciones = []

    for nodo in nodelist:
        if isinstance(nodo, LatexCharsNode):
            fragmento = nodo.chars.strip()
            if fragmento:
                texto_normal.append(fragmento)

        elif isinstance(nodo, LatexMathNode):
            contenido = texto[nodo.pos:nodo.pos_end]
            ecuaciones.append(contenido.strip())

    texto_unido = " ".join(texto_normal).strip()

    return texto_unido, ecuaciones


# ------------------- Prueba ---------------------

if __name__ == "__main__":
    texto_prueba = r"""
Este es un documento sobre física cuántica.
La ecuación de Schrödinger es: $i\hbar\frac{\partial}{\partial t}\Psi = \hat{H}\Psi$
También existen expresiones como $E = mc^2$ y otras fórmulas.
Este texto debe ir como bloque normal.
"""

    texto_unido, ecuaciones_limpias = detectar_bloques_latex(texto_prueba)

    print("\n→ TEXTO UNIDO:\n", texto_unido)
    print("\n→ BLOQUES MATEMÁTICOS:")
    for eq in ecuaciones_limpias:
        print("-", eq)