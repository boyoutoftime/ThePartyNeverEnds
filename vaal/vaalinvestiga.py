# arxiv_descargador_api.py
import urllib.request
import xml.etree.ElementTree as ET
import os
import time
from datetime import datetime, timedelta

os.makedirs("pdfs", exist_ok=True)

subcategorias = [
    "astro-ph", "cond-mat", "gr-qc", "hep-ex",
    "hep-lat", "hep-ph", "hep-th", "math-ph",
    "nlin", "nucl-ex", "nucl-th", "physics", "quant-ph"
]

# Calcular fecha hace 3 meses
hoy = datetime.utcnow()
tres_meses_atras = hoy - timedelta(days=90)
desde_fecha = tres_meses_atras.strftime("%Y%m%d%H%M")  # formato: YYYYMMDDhhmm

def descargar_pdf(id_archivo, subcat):
    pdf_url = f"https://arxiv.org/pdf/{id_archivo}.pdf"
    ruta = f"pdfs/{subcat}_{id_archivo}.pdf"
    print(f"⬇️ Descargando {pdf_url}")
    try:
        urllib.request.urlretrieve(pdf_url, ruta)
        print(f"✅ Guardado como: {ruta}")
    except urllib.error.HTTPError as e:
        print(f"❌ Error {e.code}: {e.reason} al descargar {pdf_url}")

def procesar_subcategoria(subcat):
    url = (
        f"http://export.arxiv.org/api/query?"
        f"search_query=cat:{subcat}+AND+submittedDate:[{desde_fecha}+TO+*]"
        f"&sortBy=lastUpdatedDate&max_results=1"
    )

    print(f"\n📥 Consultando API: {subcat}")
    try:
        xml = urllib.request.urlopen(url).read()
    except Exception as e:
        print(f"❌ Error al consultar API: {e}")
        return

    root = ET.fromstring(xml)
    namespaces = {'atom': 'http://www.w3.org/2005/Atom'}
    entries = root.findall('atom:entry', namespaces)

    if not entries:
        print("⚠️ No se encontraron artículos recientes.")
        return

    entry = entries[0]
    id_full = entry.find('atom:id', namespaces).text
    id_archivo = id_full.split('/')[-1]

    # Saltar IDs del formato antiguo (tienen slash en el ID)
    if '/' in id_archivo:
        print(f"⏭️ ID antiguo detectado: {id_archivo}, se omite.")
        return

    print(f"🧠 ID encontrado: {id_archivo}")
    descargar_pdf(id_archivo, subcat)
    time.sleep(2)

if __name__ == "__main__":
    for subcat in subcategorias:
        procesar_subcategoria(subcat)