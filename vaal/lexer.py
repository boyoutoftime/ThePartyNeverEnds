from pylatexenc.latexwalker import LatexWalker, LatexCharsNode, LatexMathNode

def detectar_bloques_latex(texto):
    walker = LatexWalker(texto)
    nodelist, *_ = walker.get_latex_nodes(pos=0)

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