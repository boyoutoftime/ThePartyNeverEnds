from pylatexenc.latexwalker import LatexWalker, LatexMathNode

def detectar_bloques_latex(texto):
    walker = LatexWalker(texto)
    nodos = walker.get_latex_nodes()  # ← Corrección aquí

    bloques_matematicos = []
    bloques_texto = []

    for nodo in nodos:
        contenido = texto[nodo.pos:nodo.pos_end]
        if isinstance(nodo, LatexMathNode):
            bloques_matematicos.append(contenido.strip())
        else:
            bloques_texto.append(contenido.strip())

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
    print("-", t)

print("\n→ BLOQUES MATEMÁTICOS:")
for e in ecuaciones:
    print("-", e)