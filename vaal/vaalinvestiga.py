# archivo: arxiv_descargador.py

import urllib.request
import re
import os
import time

# Lista de subcategorías científicas
subcategorias = [
    "astro-ph", "cond-mat", "gr-qc", "hep-ex", "hep-lat", "hep-ph",
    "hep-th", "math-ph", "nlin", "nucl-ex", "nucl-th", "physics", "quant-ph"
]

# Crear carpeta de PDFs si no existe
os.makedirs("pdfs", exist_ok=True)

def descargar_pdf(abs_id, subcat):
    pdf_url = f"https://arxiv.org/pdf/{abs_id}.pdf"
    archivo = f"pdfs/{subcat}_{abs_id}.pdf"
    try:
        urllib.request.urlretrieve(pdf_url, archivo)
        print(f"✅ PDF descargado: {archivo}")
    except Exception as e:
        print(f"❌ Error al descargar {pdf_url}: {e}")

def procesar_subcategoria(subcat):
    url = f"https://arxiv.org/list/{subcat}/recent"
    print(f"\n📥 Revisando subcategoría: {url}")

    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"❌ Error al acceder a {url}: {e}")
        return

    # Buscar todos los IDs de artículos en la forma /abs/XXXX.XXXXX
    matches = re.findall(r'href="/abs/(\d{4}\.\d{5})"', html)
    if not matches:
        print("⚠️ No se encontraron artículos en esta subcategoría.")
        return

    # Evitar duplicados
    articulos = list(dict.fromkeys(matches))

    print(f"🔎 Se encontraron {len(articulos)} artículos.")
    
    # Descargar el primero (puedes cambiar para descargar varios)
    for abs_id in articulos[:1]:
        print(f"➡️ Procesando artículo {abs_id}")
        descargar_pdf(abs_id, subcat)
        time.sleep(5)  # Para no ser detectado como bot

# Ejecutar para todas las subcategorías
for subcat in subcategorias:
    procesar_subcategoria(subcat)