import requests
from bs4 import BeautifulSoup

def extraer_texto_de_url(url):
    try:
        respuesta = requests.get(url)
        if respuesta.status_code != 200:
            return ""
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        # Extraer todo el texto visible
        textos = soup.stripped_strings
        return " ".join(textos)
    except Exception as e:
        print(f"Error extrayendo texto de {url}: {e}")
        return ""