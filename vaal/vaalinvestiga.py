# arxiv_descargador_api.py
import urllib.request
import xml.etree.ElementTree as ET
import os
import time

os.makedirs("pdfs", exist_ok=True)

subcategorias = [
    "astro-ph", "cond-mat", "gr-qc", "hep-ex",
    "hep-lat", "hep-ph", "hep-th", "math-ph",
    "nlin", "nucl-ex", "nucl-th", "physics", "quant-ph"
]

def descargar_pdf(id_archivo, subcat):
    pdf_url = f"https://arxiv.org/pdf/{id_archivo}.pdf"
    ruta = f"pdfs/{subcat}_{id_archivo}.pdf"
    print(f"⬇️ Descargando {pdf_url}")
    urllib.request.urlretrieve(pdf_url, ruta)
    print(f"✅ Guardado como: {ruta}")

def procesar_subcategoria(subcat):
    url = f"http://export.arxiv.org/api/query?search_query=cat:{subcat}&sortBy=lastUpdatedDate&max_results=1"
    print(f"\n📥 Consultando API: {subcat}")
    xml = urllib.request.urlopen(url).read()
    root = ET.fromstring(xml)

    namespaces = {'atom': 'http://www.w3.org/2005/Atom'}
    entries = root.findall('atom:entry', namespaces)
    if not entries:
        print("⚠️ No se encontraron artículos en API.")
        return

    entry = entries[0]
    id_full = entry.find('atom:id', namespaces).text  # "http://arxiv.org/abs/2406.XXXXX"
    id_archivo = id_full.split('/')[-1]
    print(f"🧠 ID encontrado: {id_archivo}")
    descargar_pdf(id_archivo, subcat)
    time.sleep(2)

if __name__ == "__main__":
    for subcat in subcategorias:
        procesar_subcategoria(subcat)