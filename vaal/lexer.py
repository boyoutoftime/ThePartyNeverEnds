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
