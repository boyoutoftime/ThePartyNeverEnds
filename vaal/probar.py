from lector import extraer_texto_de_pdf
import sys

def porcentaje_ruido(texto):
    total = len(texto)
    if total == 0:
        return 100
    caracteres_raros = sum(1 for c in texto if ord(c) > 126 or ord(c) < 32 and c not in '\n\t\r')
    return (caracteres_raros / total) * 100

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python test_pdf_ruidoso.py archivo.pdf")
        sys.exit(1)

    ruta = sys.argv[1]
    print(f"🧪 Analizando ruido en: {ruta}")
    texto = extraer_texto_de_pdf(ruta)
    ruido = porcentaje_ruido(texto)
    print(f"🔎 Porcentaje de ruido: {ruido:.2f}%")

    if ruido > 30:
        print("⚠️ El PDF contiene demasiado ruido. Se recomienda descartarlo.")
    else:
        print("✅ El PDF parece legible.")