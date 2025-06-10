import requests
from bs4 import BeautifulSoup

def buscar_en_duckduckgo(tema: str, max_resultados=5):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f"https://html.duckduckgo.com/html/?q={tema}"

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    resultados = []
    for link in soup.find_all('a', attrs={'class': 'result__a'}, limit=max_resultados):
        href = link.get('href')
        resultados.append(href)

    return resultados