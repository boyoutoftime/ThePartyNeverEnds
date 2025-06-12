import fitz  # PyMuPDF
import regex as re
import sys
import os
import json


# === Regex avanzada para detectar fragmentos matemáticos en texto plano ===
ECUACION_REGEX = r"""
(?<!\w)                             # no carácter alfabético antes
(?:
    [A-Za-z]*\s*=\s*[-+*/^A-Za-z0-9.()]+      # expresiones tipo α = 0.73 ± 0.02
  | [A-Za-z]+\^\d+                 # potencias tipo x^2, A^3
  | [A-Za-z]+\_\{?[0-9a-zA-Z]+\}?  # subíndices tipo N_{i}, x_1
  | [A-Za-z]+\s*∝\s*[A-Za-z0-9/]+ # proporcionales: P ∝ ADp/2
  | \b[A-Za-z0-9]+/[A-Za-z0-9]+\b # divisiones con slash: ADp/2
)
(?![\w-])                          # no seguir con palabra o guión
"""

REGEX_ECUACION = re.compile(ECUACION_REGEX, re.VERBOSE)

def extraer_texto_del_pdf(pdf_path):
    texto_completo = ""
    doc = fitz.open(pdf_path)
    for pagina in doc:
        texto_completo += pagina.get_text()
    return texto_completo

def detectar_fragmentos(texto):
    candidatos = []
    lineas = texto.split("\n")
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        ecuaciones = REGEX_ECUACION.findall(linea)
        if ecuaciones:
            candidatos.append({
                "original": linea,
                "ecuaciones": ecuaciones
            })
    return candidatos

def guardar_salida(candidatos, archivo_salida):
    with open(archivo_salida, "w", encoding="utf-8") as f:
        json.dump(candidatos, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python extractor.py archivo.pdf")
        sys.exit(1)

    archivo_pdf = sys.argv[1]
    if not os.path.exists(archivo_pdf):
        print(f"[ERROR] Archivo no encontrado: {archivo_pdf}")
        sys.exit(1)

    print(f"[INFO] Extrayendo texto de: {archivo_pdf}")
    texto = extraer_texto_del_pdf(archivo_pdf)

    print("[INFO] Detectando fragmentos candidatos...")
    fragmentos = detectar_fragmentos(texto)

    archivo_salida = archivo_pdf.replace(".pdf", "_fragmentos.json")
    guardar_salida(fragmentos, archivo_salida)

    print(f"[OK] Fragmentos guardados en: {archivo_salida}")
    print(f"[TOTAL]: {len(fragmentos)} fragmentos encontrados.")