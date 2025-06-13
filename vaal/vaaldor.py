
# vaaldor.py

from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os
import sys

# --- CONFIGURACIÓN --- #
PDF_PATH = "documento.pdf"    # Cambia por el nombre de tu archivo PDF
DPI = 300                     # Resolución de conversión (300 recomendado para OCR)
OUTPUT_FOLDER = "paginas_img"  # Carpeta donde se guardan las imágenes (puede ser temporal)

# --- FUNCIÓN: Convertir PDF a imágenes --- #
def convertir_pdf_a_imagenes(pdf_path, dpi=300):
    print(f"[+] Convirtiendo PDF a imágenes (DPI: {dpi})...")
    paginas = convert_from_path(pdf_path, dpi=dpi)
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    rutas_imagenes = []
    for i, pagina in enumerate(paginas):
        ruta = os.path.join(OUTPUT_FOLDER, f"pagina_{i+1}.png")
        pagina.save(ruta, "PNG")
        rutas_imagenes.append(ruta)

    print(f"[+] {len(rutas_imagenes)} páginas convertidas a imágenes.")
    return rutas_imagenes

# --- FUNCIÓN: Realizar OCR y extraer líneas --- #
def extraer_lineas_por_ocr(ruta_imagen):
    print(f"[OCR] Analizando: {ruta_imagen}")
    imagen = Image.open(ruta_imagen)
    datos = pytesseract.image_to_data(
    imagen,
    lang="eng",  # Aquí defines los idiomas que deseas usar
    output_type=pytesseract.Output.DICT
)

    lineas = {}
    for i in range(len(datos['text'])):
        palabra = datos['text'][i].strip()
        if palabra == "":
            continue

        linea = datos['line_num'][i]
        if linea not in lineas:
            lineas[linea] = []

        lineas[linea].append({
            "texto": palabra,
            "left": datos['left'][i],
            "top": datos['top'][i],
            "width": datos['width'][i],
            "height": datos['height'][i],
            "conf": int(datos['conf'][i])
        })

    return lineas

# --- FUNCIÓN PRINCIPAL --- #
def procesar_pdf(pdf_path):
    rutas = convertir_pdf_a_imagenes(pdf_path, dpi=DPI)

    for num_pagina, ruta_img in enumerate(rutas, start=1):
        print(f"\n===== PÁGINA {num_pagina} =====")
        lineas = extraer_lineas_por_ocr(ruta_img)

        for num_linea, palabras in lineas.items():
            # Filtramos palabras de baja confianza
            palabras_confiables = [p['texto'] for p in palabras if p['conf'] > 50]
            if palabras_confiables:
                texto_linea = " ".join(palabras_confiables)
                print(f"Línea {num_linea}: {texto_linea}")

# --- EJECUCIÓN --- #
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python vaaldor.py ruta/al/archivo.pdf")
        sys.exit(1)

    PDF_PATH = sys.argv[1]
    procesar_pdf(PDF_PATH)