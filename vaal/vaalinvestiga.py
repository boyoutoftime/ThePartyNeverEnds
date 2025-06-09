# archivo: arxiv_descargador.py

import urllib.request
import re
import os
import time

# Subcategorías científicas
subcategorias = [
    "astro-ph", "cond-mat", "gr-qc", "hep-ex", "hep-lat", "hep-ph",
    "hep-th", "math-ph", "nlin", "nucl-ex", "nucl-th", "physics", "quant-ph"
]

# Crear carpeta si no existe
os.makedirs("pdfs", exist_ok=True)

def descargar_pdf(abs_id, subcat):
    pdf_url = f"https://arxiv.org/pdf/{abs_id}.pdf"
    archivo_local = f"pdfs/{subcat}_{abs_id}.pdf"
    try:
        print(f"⬇️ Descargando PDF: {pdf_url}")
        urllib.request.urlretrieve(pdf_url, archivo_local)
        print(f"✅ Guardado como: {archivo_local}")
    except Exception as e:
        print(f"❌ Error al descargar {pdf_url}: {e}")

def procesar_subcategoria(subcat):
    url = f"https://arxiv.org/list/{subcat}/recent"
    print(f"\n🔎 Visitando: {url}")

    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode("utf-8")
    except Exception as e:
        print(f"❌ Error al abrir {url}: {e}")
        return

    # Buscar todos los ID del tipo arXiv:2406.00493
    ids = re.findall(r'href="/abs/(\d{4}\.\d{5})"', html)

    if not ids:
        print("⚠️ No se encontraron artículos recientes.")
        return

    # Eliminar duplicados (por si se repiten)
    ids = list(dict.fromkeys(ids))
    print(f"📄 Artículos encontrados: {len(ids)}")

    # Descargar el primero
    for abs_id in ids[:1]:
        descargar_pdf(abs_id, subcat)
        time.sleep(2)

# Ejecutar sobre todas las subcategorías
for subcat in subcategorias:
    procesar_subcategoria(subcat)