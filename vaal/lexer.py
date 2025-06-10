from pylatexenc.latexwalker import LatexWalker

def detectar_bloques_latex(texto):
    walker = LatexWalker(texto)
    nodelist, parsing_errors = walker.get_latex_nodes(pos=0)

    bloques_matematicos = []
    texto_normal = []
    for nodo in nodelist:
        contenido = texto[nodo.pos:nodo.pos_end]
        if nodo.isNodeType('LatexMathNode'):
            bloques_matematicos.append(contenido)
        else:
            texto_normal.append(contenido)

    return texto_normal, bloques_matematicos

if __name__ == "__main__":
    texto = r"""
    Este es un documento sobre física cuántica.
    La ecuación de Schrödinger es: i\hbar \frac{\partial}{\partial t} \Psi = \hat{H} \Psi
    También existen expresiones como $E=mc^2$ y otras fórmulas.
    """

    resultado = detectar_bloques_latex(texto)

    print("→ TEXTO NORMAL:")
    print(resultado['texto'])
    print("\n→ BLOQUES MATEMÁTICOS:")
    print(resultado['matematico'])
    print("\n→ RUIDO DETECTADO:")
    print(resultado['ruido'])