from pylatexenc.latexwalker import (
    LatexWalker, LatexNode, LatexCharsNode,
    LatexMathNode, LatexGroupNode, LatexMacroNode
)

def nodo_a_texto(nodo):
    if isinstance(nodo, LatexCharsNode):
        return nodo.chars

    elif isinstance(nodo, LatexMacroNode):
        # Si tiene argumentos (como \frac{...}{...})
        args = ''
        if nodo.nodeargd and nodo.nodeargd.argnlist:
            args = ''.join(
                '{' + nodo_a_texto(arg) + '}' for arg in nodo.nodeargd.argnlist
            )
        return '\\' + nodo.macroname + args

    elif isinstance(nodo, LatexGroupNode):
        # Grupo del tipo {...}
        return ''.join(nodo_a_texto(n) for n in nodo.nodelist)

    elif isinstance(nodo, LatexMathNode):
        return ''.join(nodo_a_texto(n) for n in nodo.nodelist)

    elif hasattr(nodo, 'nodelist'):
        return ''.join(nodo_a_texto(n) for n in nodo.nodelist)

    return ''  # Fallback para tipos desconocidos

def detectar_bloques_latex(texto):
    walker = LatexWalker(texto)
    nodos, _ = walker.get_latex_nodes(pos=0)  # ← Esta línea funciona con tu versión

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
for e in ecuaciones:
    print("-", e.strip())