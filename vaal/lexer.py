from pylatexenc.latexwalker import LatexWalker, LatexMathNode, LatexCharsNode

def nodo_a_texto(nodo):
    """
    Convierte un nodo Latex a texto plano, recursivamente si es necesario.
    """
    if isinstance(nodo, LatexCharsNode):
        return nodo.chars
    elif isinstance(nodo, LatexMathNode):
        # Para nodos matemáticos, concatenamos recursivamente su nodelist
        return ''.join(nodo_a_texto(n) for n in nodo.nodelist)
    else:
        # Para otros nodos (macros, grupos), intentamos extraer texto de sus hijos
        if hasattr(nodo, 'nodelist'):
            return ''.join(nodo_a_texto(n) for n in nodo.nodelist)
        return ''

def detectar_bloques_latex(texto):
    walker = LatexWalker(texto)
    resultado = walker.get_latex_nodes(pos=0)

    if isinstance(resultado, tuple):
        nodos = resultado[0]
    else:
        nodos = resultado

    bloques_matematicos = []
    bloques_texto = []

    for nodo in nodos:
        if isinstance(nodo, LatexMathNode):
            bloques_matematicos.append(nodo_a_texto(nodo))
        elif isinstance(nodo, LatexCharsNode):
            bloques_texto.append(nodo.chars)
        else:
            # Podrías considerar si quieres procesar más tipos de nodos aquí
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
for e in ecuaciones:
    print("-", e.strip())