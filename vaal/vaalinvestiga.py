# archivo: arxiv_descargador.py

import urllib.request
import re
import os
import time

# Subcategorías a explorar
subcategorias = [
    "astro-ph", "cond-mat", "gr-qc", "hep-ex", "hep-lat", "hep-ph",
    "hep-th", "math-ph", "nlin", "nucl-ex", "nucl-th", "physics", "quant-ph"
]

# Carpeta para guardar los PDFs
os.makedirs("pdfs", exist_ok=True)

def descargar_pdf(abs_id, subcat):
    pdf_url = f"https://arxiv.org/pdf/{abs_id}.pdf"
    archivo = f"pdfs/{subcat}_{abs_id}.pdf"
    try:
        print(f"➡️ Descargando PDF desde: {pdf_url}")
        urllib.request.urlretrieve(pdf_url, archivo)
        print(f"✅ PDF guardado en: {archivo}")
    except Exception as e:
        print(f"❌ Error al descargar PDF: {e}")

def procesar_subcategoria(subcat):
    url = f"https://arxiv.org/list/{subcat}/recent"
    print(f"\n📥 Revisando subcategoría: {url}")

    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"❌ Error al acceder a {url}: {e}")
        return

    # Buscar todos los enlaces /abs/XXXX.XXXXX
    articulos = re.findall(r'href="/abs/(\d{4}\.\d{5})"', html)

    if not articulos:
        print("⚠️ No se encontraron artículos en esta subcategoría.")
        return

    articulos = list(dict.fromkeys(articulos))  # quitar duplicados
    print(f"📚 Se encontraron {len(articulos)} artículos")

    # Descargar el primero (puedes cambiar a varios)
    for abs_id in articulos[:1]:
        descargar_pdf(abs_id, subcat)
        time.sleep(3)  # pausa para evitar ser bloqueado

# Revisar todas las subcategorías
for subcat in subcategorias:
    procesar_subcategoria(subcat)