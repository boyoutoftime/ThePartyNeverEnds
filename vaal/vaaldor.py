from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import sys

DPI = 300

def convertir_pdf_a_imagenes_en_memoria(pdf_path, dpi=300):
    print(f"[+] Convirtiendo PDF a imágenes en memoria (DPI: {dpi})...")
    paginas = convert_from_path(pdf_path, dpi=dpi)
    print(f"[+] {len(paginas)} páginas convertidas a imágenes en memoria.")
    return paginas

def extraer_lineas_por_ocr_imagen(imagen, idioma):
    datos = pytesseract.image_to_data(
        imagen,
        lang=idioma,
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

def procesar_pdf_en_memoria(pdf_path, idioma):
    paginas = convertir_pdf_a_imagenes_en_memoria(pdf_path, dpi=DPI)

    for num_pagina, imagen in enumerate(paginas, start=1):
        print(f"\n===== PÁGINA {num_pagina} =====")
        lineas = extraer_lineas_por_ocr_imagen(imagen, idioma)

        for num_linea, palabras in lineas.items():
            palabras_confiables = [p['texto'] for p in palabras if p['conf'] > 50]
            if palabras_confiables:
                texto_linea = " ".join(palabras_confiables)
                print(f"Línea {num_linea}: {texto_linea}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python vaaldor.py ruta/al/archivo.pdf [idioma]")
        sys.exit(1)

    PDF_PATH = sys.argv[1]
    idioma = sys.argv[2] if len(sys.argv) > 2 else "eng"
    procesar_pdf_en_memoria(PDF_PATH, idioma)