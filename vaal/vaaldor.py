from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import sys
import multiprocessing
from io import BytesIO

# --- CONFIGURACIÓN --- #
DPI = 300
NUM_PROCESOS = 4  # Número de núcleos a usar

def convertir_pdf_a_bytes(pdf_path, dpi=300):
    print(f"[+] Convirtiendo PDF a imágenes en memoria (DPI: {dpi})...")
    paginas = convert_from_path(pdf_path, dpi=dpi)
    imagenes_en_bytes = []

    for num_pagina, pagina in enumerate(paginas, start=1):
        buffer = BytesIO()
        pagina.save(buffer, format="PNG")
        imagen_bytes = buffer.getvalue()
        imagenes_en_bytes.append((imagen_bytes, num_pagina))
        buffer.close()

    print(f"[+] {len(imagenes_en_bytes)} páginas convertidas a imágenes (en memoria).")
    return imagenes_en_bytes

def extraer_lineas_por_ocr_en_memoria(args):
    imagen_bytes, idioma, num_pagina = args
    print(f"[OCR] Analizando página {num_pagina} (en memoria)...")
    
    imagen = Image.open(BytesIO(imagen_bytes))
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
    imagenes_en_memoria = convertir_pdf_a_bytes(pdf_path, dpi=DPI)

    # Preparar argumentos para multiproceso
    args = [(imagen_bytes, idioma, num_pagina) for imagen_bytes, num_pagina in imagenes_en_memoria]

    with multiprocessing.Pool(NUM_PROCESOS) as pool:
        resultados = pool.map(extraer_lineas_por_ocr_en_memoria, args)

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