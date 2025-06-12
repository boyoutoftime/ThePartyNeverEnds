import fitz  # PyMuPDF
import regex as re
import sys
import os
import json

# === Regex avanzada para detectar fragmentos matemáticos en texto plano ===
REGEX_ECUACION = re.compile(r"""
    (?<!\w)                # no debe haber letra justo antes
    (                     # comienzo de grupo
        [\w\d]*?          # posibles variables
        (?:[+\-*/^=]|\\pm|\\cdot|\\leq|\\geq|\\int|\\sum|\\frac|∑|∫)+   # símbolos matemáticos
        [\w\d()^_\\]+     # más símbolos, variables o funciones
    )
    (?!\w)                # no debe haber letra justo después
""", re.VERBOSE)

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