# Módulo que realiza el mapeo de id a nombre y escribe un json respectivo
# con la metadata de cada diputado
# Utiliza el html de la url https://www.camara.cl/diputados/diputados.aspx#mostrarDiputados 

from bs4 import BeautifulSoup as Bs
import unicodedata
import json

BASE_HTML = '../data/mostrarDiputados.html'
JSON_PATH = '../data/diputados_metadata.json'


def write_json(filename, data):
    with open(filename, 'w+') as outfile:
        json.dump(data, outfile, ensure_ascii=False)

def extract_metadata(raw_html):
    parser = Bs(raw_html, 'html.parser')
    articles = parser.find_all("article", class_="grid-2")
    metadata = {}
    for article in articles:
        diputadoId = article.h4.a['href'].split('=')[1]
        diputadoName = article.h4.a.text.split('. ')[1]
        distrito = article.find_all('p')[0].text.split(': ')[1]
        partido = article.find_all('p')[1].text.split(': ')[1]
        metadata[diputadoId] = {
            'nombre':  diputadoName,
            'distrito': distrito,
            'partido':  partido
        }
    return metadata
    

if __name__ == "__main__":
    with open(BASE_HTML, 'r') as raw_html:
        metadata = extract_metadata(raw_html)
        write_json(JSON_PATH, metadata)
    

