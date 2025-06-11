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

if __name__ == "__main__":
    texto_de_prueba = (
        "Este es un texto con una ecuación inline $E=mc^2$ "
        "y otra en modo display: \\\int_0^\\infty e^{-x} dx = 1 \. "
        "Además, hay más texto al final."
    )

    texto, ecuaciones = detectar_bloques_latex(texto_de_prueba)

    print("Texto normal:")
    print(texto)
    print("\nEcuaciones encontradas:")
    for i, eq in enumerate(ecuaciones, 1):
        print(f"{i}: {eq}")