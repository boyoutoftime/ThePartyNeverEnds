# vaalinvestiga.py
import urllib.request
import xml.etree.ElementTree as ET
import os
import time
from datetime import datetime, timedelta, timezone

os.makedirs("pdfs", exist_ok=True)

subcategorias = [
    "astro-ph.GA"
]

hoy = datetime.now(timezone.utc)
tres_meses_atras = hoy - timedelta(days=90)

def descargar_pdf(id_archivo, subcat):
    if '.' in id_archivo:
        # ID moderno (después de 2007)
        url_pdf = f"https://arxiv.org/pdf/{id_archivo}.pdf"
        nombre_archivo = id_archivo.replace('/', '_')
    else:
        # ID antiguo (antes de 2007) → necesita la subcategoría
        url_pdf = f"https://arxiv.org/pdf/{subcat}/{id_archivo}.pdf"
        nombre_archivo = f"{subcat}_{id_archivo}"

    ruta = f"pdfs/{nombre_archivo}.pdf"

    print(f"⬇️ Descargando {url_pdf}")
    try:
        urllib.request.urlretrieve(url_pdf, ruta)
        print(f"✅ Guardado como: {ruta}")
    except urllib.error.HTTPError as e:
        print(f"❌ Error {e.code}: {e.reason} al descargar {url_pdf}")

def procesar_subcategoria(subcat):
    url = (
        f"http://export.arxiv.org/api/query?"
        f"search_query=cat:{subcat}&sortBy=lastUpdatedDate&max_results=5"
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
        print("⚠️ No se encontraron artículos.")
        return

    encontrados = 0
    for entry in entries:
        fecha_str = entry.find('atom:updated', namespaces).text
        fecha = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

        if fecha < tres_meses_atras:
            continue  # ignorar artículos viejos

        id_full = entry.find('atom:id', namespaces).text
        id_archivo = id_full.split('/')[-1]

        print(f"🧠 ID reciente encontrado: {id_archivo}")
        descargar_pdf(id_archivo, subcat)
        encontrados += 1
        time.sleep(2)

    if encontrados == 0:
        print("⚠️ No se encontraron artículos recientes.")

if __name__ == "__main__":
    for subcat in subcategorias:
        procesar_subcategoria(subcat)