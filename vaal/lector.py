import requests
from bs4 import BeautifulSoup

def extraer_texto_de_url(url):
    try:
        respuesta = requests.get(url)
        if respuesta.status_code != 200:
            return ""
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        textos = soup.stripped_strings
        return " ".join(textos)
    except Exception as e:
        print(f"Error extrayendo texto de {url}: {e}")
        return ""

def extraer_texto_de_pdf(ruta_pdf):
    texto = ""
    try:
        with open(ruta_pdf, 'rb') as f:
            contenido = f.read()
            try:
                texto = contenido.decode('utf-8')
            except UnicodeDecodeError:
                texto = contenido.decode('latin1', errors='ignore')
    except Exception as e:
        print(f"Error leyendo PDF {ruta_pdf}: {e}")
    return texto