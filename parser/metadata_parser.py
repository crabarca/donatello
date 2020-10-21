# Módulo que realiza el mapeo de id a nombre y escribe un json respectivo
# con la metadata de cada diputado
# Utiliza el html de la url https://www.camara.cl/diputados/diputados.aspx#mostrarDiputados 

from bs4 import BeautifulSoup as Bs
import unicodedata
import json
import csv
from pathlib import Path

BASE_HTML = Path('../data/mostrarDiputados.html')
JSON_PATH = Path('../data/diputados_metadata.json')
CSV_PATH = Path('../data/diputados_metadata.csv')

def write_json(filename, data):
    with open(filename, 'w+') as outfile:
        json.dump(data, outfile, ensure_ascii=False)

def write_csv(filename, header, rows):
    with open(filename, 'w+') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(rows)

def extract_metadata_json(raw_html):
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

def extract_metadata_csv(raw_html):
    parser = Bs(raw_html, 'html.parser')
    header = ['ID', 'NOMBRE', 'DISTRITO', 'PARTIDO']
    rows = []
    articles = parser.find_all("article", class_="grid-2")
    for article in articles:
        diputadoId = article.h4.a['href'].split('=')[1]
        diputadoName = article.h4.a.text.split('. ')[1]
        distrito = article.find_all('p')[0].text.split(': ')[1]
        partido = article.find_all('p')[1].text.split(': ')[1]
        print(diputadoName)
        rows.append([diputadoId, diputadoName, distrito, partido])
    return header, rows
    
if __name__ == "__main__":
    with open(BASE_HTML, 'r') as raw_html:
        # metadata_json = extract_metadata_json(raw_html)
        header, rows = extract_metadata_csv(raw_html)
        write_csv(CSV_PATH, header, rows)
        # write_json(JSON_PATH, metadata)

    

