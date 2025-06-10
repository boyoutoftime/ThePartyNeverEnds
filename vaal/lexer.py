from pygments.lexers import TexLexer
from pygments.token import Token
from pygments import lex

def clasificar_bloques(texto):
    bloques = {
        'matematico': [],
        'texto': [],
        'ruido': []
    }

    for token_tipo, valor in lex(texto, TexLexer()):
        valor = valor.strip()
        if not valor:
            continue

        if token_tipo in Token.String:  # Texto normal en LaTeX
            bloques['texto'].append(valor)

        elif token_tipo in Token.Name or token_tipo in Token.Keyword:
            bloques['matematico'].append(valor)

        elif token_tipo in Token.Comment or token_tipo in Token.Other:
            bloques['ruido'].append(valor)

        else:
            bloques['ruido'].append(valor)

    return bloques

if __name__ == "__main__":
    texto = r"""
    Este es un documento sobre física cuántica.
    La ecuación de Schrödinger es: i\hbar \frac{\partial}{\partial t} \Psi = \hat{H} \Psi
    También existen expresiones como $E=mc^2$ y otras fórmulas.
    """

    resultado = clasificar_bloques(texto)

    print("→ TEXTO NORMAL:")
    print(resultado['texto'])
    print("\n→ BLOQUES MATEMÁTICOS:")
    print(resultado['matematico'])
    print("\n→ RUIDO DETECTADO:")
    print(resultado['ruido'])