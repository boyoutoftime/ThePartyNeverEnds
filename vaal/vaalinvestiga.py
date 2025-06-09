
import urllib.request
import re
import os
import time

subcategorias = [
    "astro-ph", "cond-mat", "gr-qc", "hep-ex", "hep-lat", "hep-ph",
    "hep-th", "math-ph", "nlin", "nucl-ex", "nucl-th", "physics", "quant-ph"
]

os.makedirs("pdfs", exist_ok=True)

def descargar_pdf(subcat):
    url = f"https://arxiv.org/list/{subcat}/recent"
    print(f"📥 Revisando: {url}")

    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"❌ Error al acceder a {subcat}: {e}")
        return

    # Buscar la primera ID de artículo
    matches = re.findall(r'href="/abs/(\d+\.\d+)"', html)
    if not matches:
        print("⚠️ No se encontró ningún artículo.")
        return

    articulo_id = matches[0]
    pdf_url = f"https://arxiv.org/pdf/{articulo_id}.pdf"
    pdf_ruta = f"pdfs/{subcat}_{articulo_id}.pdf"

    # Descargar el PDF
    try:
        urllib.request.urlretrieve(pdf_url, pdf_ruta)
        print(f"✅ PDF guardado: {pdf_ruta}")
    except Exception as e:
        print(f"❌ Error al descargar PDF: {e}")

    time.sleep(5)  # Pausa para simular comportamiento humano


# Ejecutar descarga para todas las subcategorías
for subcat in subcategorias:
    descargar_pdf(subcat)