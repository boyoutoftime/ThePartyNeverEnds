from pylatexenc.latexwalker import LatexWalker, LatexCharsNode, LatexMathNode

def nodo_a_texto(nodo):
    try:
        return nodo.latex_verbatim()
    except AttributeError:
        return str(nodo)

def detectar_bloques_latex(texto):
    walker = LatexWalker(texto)
    result = walker.get_latex_nodes(pos=0)
    nodos = result[0]

    bloques_matematicos = []
    bloques_texto = []

    for nodo in nodos:
        if isinstance(nodo, LatexMathNode):
            bloques_matematicos.append(nodo_a_texto(nodo))
        elif isinstance(nodo, LatexCharsNode):
            bloques_texto.append(nodo.chars)
        else:
            bloques_texto.append(nodo_a_texto(nodo))

    return bloques_texto, bloques_matematicos

# Prueba
texto_prueba = r"""
Este es un documento sobre física cuántica.
La ecuación de Schrödinger es: $i\hbar\frac{\partial}{\partial t}\Psi = \hat{H}\Psi$
También existen expresiones como $E = mc^2$ y otras fórmulas.
Este texto debe ir como bloque normal.
"""

texto, ecuaciones = detectar_bloques_latex(texto_prueba)

print("→ TEXTO NORMAL:")
for t in texto:
    print("-", t.strip())

print("\n→ BLOQUES MATEMÁTICOS:")
for eq in ecuaciones:
    print("-", eq.strip())