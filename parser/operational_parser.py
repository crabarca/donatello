from bs4 import BeautifulSoup as Bs
from pathlib import Path
import json
import logging
import unicodedata
import os

RAW_HTML = "../data/Honorable Cámara de Diputadas y Diputados - Chile.html"
RAW_FILES = Path("../data/raw/").glob("**/*")
METADATA_FILE = Path("../data/diputados_metadata.json")

def extract_table(raw_html):
    """
        Extrae la información desde la tabla en html 
        Retorna: 
        Tabla con headers y datos en formato lista
    """
    parser = Bs(raw_html, 'html.parser')
    table = parser.find('table', {"class": 'tabla'})
    if table:
        th = table.find_all('th')
        headers = [clean_text(header.string) for header in th]
        rows = []
        for row in table.find_all('tr'):
            rows.append([clean_text(val.string) for val in row.find_all('td')])
        return headers, rows
    else:
        return [], []

def extract_operational_data(raw_html):
    """
        Desde los datos raw se extraen las columnas 
    """
    headers, rows = extract_table(raw_html)
    if not headers or not rows:
        return [], []

    # Por alguna razon a alguien le parecio una excelente idea
    # dejar una columna extra con espacios en blancos
    clean_rows = [row for row in rows if row != []]
    transposed = [list(row) for row in zip(*clean_rows)]

    # Reemplazar los 223.234 por 223234
    header, row = transposed[0], list(map(lambda s: s.replace('.', ''), transposed[1]))
    return header, row 

# def parse_year(raw_html):
#     parser = Bs(raw_html, 'html.parser')
#     selector = parser.select("#ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlAno > option[selected='selected']")
#     return selector[0].text

# def parse_month(raw_html):
#     parser = Bs(raw_html, 'html.parser')
#     selector = parser.select("#ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlMes > option[selected='selected']")
#     return selector[0].text

def clean_text(text):
    # Por alguna razon el texto esta bastante sucio  con unicode chars y espacios
    return unicodedata.normalize("NFKD", text).replace('\n', '').strip()

def write_json(filename, data):
    pass

def split_filename(file: Path):
    return file.stem.split('_')


if __name__ == "__main__":
    htmls = [html.resolve() for html in RAW_FILES if html.is_file()]

    with open(METADATA_FILE, 'r') as f:
        metadata = json.load(f)
        
        for html in htmls[:10]:
            with open(html, 'r') as raw_html:
                header, rows = extract_operational_data(raw_html)
                data = dict(zip(header, rows))


