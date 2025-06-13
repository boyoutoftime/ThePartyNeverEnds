from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os
import sys
import multiprocessing

# --- CONFIGURACIÓN --- #
DPI = 300
OUTPUT_FOLDER = "paginas_img"
NUM_PROCESOS = 5  # Usar 5 núcleos

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

def extraer_lineas_por_ocr(args):
    ruta_imagen, idioma, num_pagina = args
    print(f"[OCR] Analizando página {num_pagina}: {ruta_imagen}")
    imagen = Image.open(ruta_imagen)
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

    return (num_pagina, lineas)

def procesar_pdf(pdf_path, idioma):
    rutas = convertir_pdf_a_imagenes(pdf_path, dpi=DPI)

    # Preparar argumentos para map
    args = [(ruta, idioma, num+1) for num, ruta in enumerate(rutas)]

    with multiprocessing.Pool(NUM_PROCESOS) as pool:
        resultados = pool.map(extraer_lineas_por_ocr, args)

    # Ordenar resultados por número de página
    resultados.sort(key=lambda x: x[0])

    for num_pagina, lineas in resultados:
        print(f"\n===== PÁGINA {num_pagina} =====")
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
    procesar_pdf(PDF_PATH, idioma)