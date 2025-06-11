from pylatexenc.latexwalker import LatexWalker, LatexCharsNode, LatexMathNode, LatexEnvironmentNode, LatexGroupNode
from pylatexenc.latexwalker import default_macro_dict, default_env_dict, MacroStandardArgsParser

def detectar_bloques_latex(texto):
    walker = LatexWalker(
        texto,
        macro_dict=default_macro_dict,
        env_dict=default_env_dict,
        math_mode_delimiters=[
            ('$', '$'),             # inline
            ('\', '\'),         # display
            ('$$', '$$'),           # display alternative
        ]
    )
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