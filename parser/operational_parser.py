from bs4 import BeautifulSoup as Bs
from pathlib import Path
import json
import logging
import unicodedata
import os
import csv

RAW_FILES = Path("../data/raw/").glob("**/*")
METADATA_FILE = Path("../data/diputados_metadata.json")
OPERATIONAL_METADATA = Path("../data/operational_metadata.json")
PROCESSED_FOLDER = Path("../data/processed")
UNIFIED_CSV = Path("../data/processed/gasto_operacional.csv")

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
        Desde los archivos html se extraen las columnas con datos
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
    with open(filename, 'w+') as outfile:
        json.dump(data, outfile, ensure_ascii=False)

def split_filename(file: Path):
    return file.stem.split('_')

def write_csv(file: Path, header, row):
    with open(file, 'r') as f:
        writer = csv.writer(f)
        # writer.r

def operational_metadata(file_list):
    # Función que se utiliza para extraer todas las posibles
    # columnas que existen en las tablas
    columns = {}
    for html in file_list:
        with open(html, 'r') as raw:
            header, rows = extract_operational_data(raw)
            for name, idx in enumerate(header):
                columns[name] = idx

    return { 'columns' : columns }

def filename_metadata(file: Path):
    return [item for item in file.stem.split('_')]

def write_csv_header(file: Path, header):
    header.insert(0, 'ANO')
    header.insert(1, 'MES')
    header.insert(2, 'ID')
    with open(file, 'a+') as f:
        writer = csv.writer(f)
        writer.writerow(header)


def table_to_csv(name, header, row):
  filepath = f"/home/cristobal/repos2/donatello/scrapper/data/{name}.csv"
  csv_file = Path(filepath)
  if csv_file.is_file():
    with open(filepath, 'a+') as f:
      writer = csv.writer(f)
      writer.writerow(row)
  else:
    with open(filepath, 'a+') as f:
      writer = csv.writer(f)
      writer.writerow(header)
      writer.writerow(row)


if __name__ == "__main__":
    htmls = [html.resolve() for html in RAW_FILES if html.is_file()]
    if not OPERATIONAL_METADATA.is_file():
        write_json(OPERATIONAL_METADATA, operational_metadata(htmls))
    else:
        metadata = []
        with open(OPERATIONAL_METADATA, 'r') as infile:
            metadata = json.load(infile)
    if not UNIFIED_CSV.is_file():
        with open(OPERATIONAL_METADATA, 'r') as f:
            # print(list(json.load(f)['columns'].values()))
            column_names = list(json.load(f)['columns'].values())
            write_csv_header(UNIFIED_CSV, column_names)
    
    # with open(METADATA_FILE, 'r') as f:
    #     metadata = json.load(f)
        
    #     for html in htmls[:10]:
    #         with open(html, 'r') as raw_html:
    #             header, rows = extract_operational_data(raw_html)
    #             data = dict(zip(header, rows))


