# archivo: arxiv_descargador.py

import urllib.request
import re
import os
import time

subcategorias = [
    "astro-ph", "cond-mat", "gr-qc", "hep-ex", "hep-lat", "hep-ph",
    "hep-th", "math-ph", "nlin", "nucl-ex", "nucl-th", "physics", "quant-ph"
]

os.makedirs("pdfs", exist_ok=True)

def descargar_pdf_desde_abs(abs_url, subcat):
    print(f"🔍 Visitando artículo: {abs_url}")
    try:
        with urllib.request.urlopen(abs_url) as response:
            html = response.read().decode("utf-8")
    except Exception as e:
        print(f"❌ Error al abrir artículo: {e}")
        return

    # Buscar el enlace al PDF dentro de la página del artículo
    match = re.search(r'href="(/pdf/\d{4}\.\d{5}(v\d+)?\.pdf)"', html)
    if match:
        pdf_path = match.group(1)
        pdf_url = "https://arxiv.org" + pdf_path
        nombre_archivo = f"pdfs/{subcat}_{pdf_path.split('/')[-1]}"
        try:
            print(f"⬇️ Descargando PDF: {pdf_url}")
            urllib.request.urlretrieve(pdf_url, nombre_archivo)
            print(f"✅ Guardado como: {nombre_archivo}")
        except Exception as e:
            print(f"❌ Error al descargar PDF: {e}")
    else:
        print("⚠️ No se encontró enlace al PDF.")

def procesar_subcategoria(subcat):
    url = f"https://arxiv.org/list/{subcat}/recent"
    print(f"\n📥 Revisando subcategoría: {url}")
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode("utf-8")
    except Exception as e:
        print(f"❌ Error al acceder a la subcategoría: {e}")
        return

    # Buscar links de artículos individuales
    enlaces_abs = re.findall(r'href="(/abs/\d{4}\.\d{5})"', html)

    if not enlaces_abs:
        print("⚠️ No se encontraron artículos.")
        return

    # Eliminar duplicados
    enlaces_abs = list(dict.fromkeys(enlaces_abs))

    # Procesar solo el primero (puedes cambiar a más si quieres)
    for enlace in enlaces_abs[:1]:
        abs_url = "https://arxiv.org" + enlace
        descargar_pdf_desde_abs(abs_url, subcat)
        time.sleep(2)

for subcat in subcategorias:
    procesar_subcategoria(subcat)