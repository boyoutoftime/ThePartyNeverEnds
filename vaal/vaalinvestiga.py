# arxiv_descargador.py

import urllib.request
import re
import os
import time

# Subcategorías de física
subcategorias = [
    "astro-ph", "cond-mat", "gr-qc", "hep-ex", "hep-lat",
    "hep-ph", "hep-th", "math-ph", "nlin", "nucl-ex",
    "nucl-th", "physics", "quant-ph"
]

os.makedirs("pdfs", exist_ok=True)

def descargar_pdf(abs_url, subcat):
    print(f"🔍 Visitando artículo: {abs_url}")
    html = urllib.request.urlopen(abs_url).read().decode("utf-8")
    match = re.search(r'href="(/pdf/\d{4}\.\d{5}(?:v\d+)?\.pdf)"', html)
    if not match:
        print("⚠️ PDF no encontrado en la página del artículo.")
        return
    pdf_url = "https://arxiv.org" + match.group(1)
    nombre = f"{subcat}_{match.group(1).split('/')[-1]}"
    ruta = os.path.join("pdfs", nombre)
    print(f"⬇️ Descargando: {pdf_url}")
    urllib.request.urlretrieve(pdf_url, ruta)
    print(f"✅ Guardado como: {ruta}")

def obtener_html(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req) as response:
        return response.read().decode("utf-8")

def procesar_subcategoria(subcat):
    url = f"https://arxiv.org/list/{subcat}/recent"
    print(f"\n📥 Revisando: {url}")
    html = obtener_html(url)  # en procesar_subcategoria
html = obtener_html(abs_url)  # en descargar_pdf
    # Extraer IDs (/abs/2406.XXXXX)
    ids = re.findall(r'href="(/abs/\d{4}\.\d{5}(?:v\d+)?)"', html)
    if not ids:
        print("⚠️ No se encontraron artículos.")
        return
    reconciliados = list(dict.fromkeys(ids))
    print(f"🧠 {len(reconciliados)} artículos listos.")
    # Procesar el primero
    descargar_pdf("https://arxiv.org" + reconciliados[0], subcat)
    time.sleep(2)

# Ejecutar rutina
for subcat in subcategorias:
    procesar_subcategoria(subcat)