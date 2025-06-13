import fitz  # PyMuPDF
import regex as re
import sys
import os
import json

# === Regex extendido para ecuaciones embebidas ===
ECUACION_REGEX = r"""
(?<![\w/])                                  # No precedido por letra/dígito/slash
(
    [A-Za-zα-ωΑ-ΩµπψφΩΨΣ∆∇θλχϕϑϵ_][\wα-ωΑ-Ω]*  # Variable inicial (e.g., ψ, αSMC)
    \s*(=|≈|≅|∝|∼|∼=|≃|≤|≥|<|>)\s*           # Operador común
    (
        (([-+±−*/^×·]?\s*[A-Za-z0-9α-ωΑ-ΩπeE.,^]+)+)
    )
)
(?![\w/])                                   # No seguido por letra/dígito/slash
"""

pattern = re.compile(ECUACION_REGEX, re.VERBOSE)

def limpiar_ecuacion(ecuacion):
    """
    Limpia una ecuación eliminando puntuación final innecesaria
    y normaliza notaciones como ×10^n o variantes.
    """
    ecuacion = ecuacion.strip()
    ecuacion = re.sub(r"[\s\.,;:)]+$", "", ecuacion)
    ecuacion = re.sub(r"×\s?10(\^?)(\d+)", r"× 10^\2", ecuacion)
    ecuacion = re.sub(r"·", "*", ecuacion)  # Convertir multiplicación implícita
    ecuacion = re.sub(r"\s+", " ", ecuacion)  # Espacios innecesarios
    return ecuacion.strip()

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

        ecuaciones_crudas = [m.group(1) for m in pattern.finditer(linea)]
        ecuaciones_limpias = [limpiar_ecuacion(e) for e in ecuaciones_crudas]

        # Eliminar duplicados dentro de la misma línea
        ecuaciones_unicas = list(sorted(set(ecuaciones_limpias)))

        if ecuaciones_unicas:
            candidatos.append({
                "original": linea,
                "ecuaciones": ecuaciones_unicas
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