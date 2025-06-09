# archivo: arxiv_descargador.py

import urllib.request
import re
import os
import time

# Subcategorías de física
subcategorias = [
    "astro-ph", "cond-mat", "gr-qc", "hep-ex", "hep-lat", "hep-ph",
    "hep-th", "math-ph", "nlin", "nucl-ex", "nucl-th", "physics", "quant-ph"
]

# Carpeta de descarga
os.makedirs("pdfs", exist_ok=True)

def descargar_pdf_desde_abs(abs_url, subcat):
    try:
        with urllib.request.urlopen(abs_url) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"❌ Error al abrir {abs_url}: {e}")
        return

    match = re.search(r'href="(\/pdf\/\d+\.\d+\.pdf)"', html)
    if not match:
        print("⚠️ No se encontró enlace PDF en la página del artículo.")
        return

    pdf_rel_url = match.group(1)
    pdf_url = f"https://arxiv.org{pdf_rel_url}"
    articulo_id = pdf_rel_url.split("/")[-1].replace(".pdf", "")
    pdf_ruta = f"pdfs/{subcat}_{articulo_id}.pdf"

    try:
        urllib.request.urlretrieve(pdf_url, pdf_ruta)
        print(f"✅ PDF guardado: {pdf_ruta}")
    except Exception as e:
        print(f"❌ Error al descargar PDF: {e}")


def procesar_subcategoria(subcat):
    url = f"https://arxiv.org/list/{subcat}/recent"
    print(f"📥 Revisando: {url}")

    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"❌ Error al acceder a {url}: {e}")
        return

    # Buscar el primer enlace a un artículo
    match = re.search(r'href="(/abs/\d+\.\d+)"', html)
    if not match:
        print("⚠️ No se encontró ningún artículo en la subcategoría.")
        return

    abs_path = match.group(1)
    abs_url = f"https://arxiv.org{abs_path}"
    print(f"🔗 Abriendo artículo: {abs_url}")

    descargar_pdf_desde_abs(abs_url, subcat)
    time.sleep(5)  # Pausa para evitar ser detectado como bot


# Ejecutar para todas las subcategorías
for subcat in subcategorias:
    procesar_subcategoria(subcat)