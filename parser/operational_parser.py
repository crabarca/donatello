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
    # dejar una columna extra con espacios
    clean_rows = [row for row in rows if row != []]
    transposed = [list(row) for row in zip(*clean_rows)]

    # Reemplazar los 223.234 por 223234
    header, row = transposed[0], list(map(lambda s: s.replace('.', ''), transposed[1]))
    return header, row
    # if len(header) == len(row):
    #     return header, row 
    # else:
    #     return [], []

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
    # Extraer todas las posibles
    # columnas que existen en las tablas
    columns = {}
    for html in file_list:
        with open(html, 'r') as raw:
            header, rows = extract_operational_data(raw)
            for idx, name in enumerate(header):
                columns[idx] = name

    return { 'columns' : columns }

def filename_metadata(file: Path):
    split = file.stem.split('_')
    if len(split) == 3:
        return dict({'ID': split[0], 'ANO': split[1], 'MES': split[2]})

def write_csv_header(file: Path, header):
    header.insert(0, 'ID')
    header.insert(1, 'ANO')
    header.insert(2, 'MES')
    with open(file, 'a+') as f:
        writer = csv.writer(f)
        writer.writerow(header)

def write_operational_data(data: dict, file_metadata: dict):
    # data_cols = list(data.keys()) 
    # data_row = list(data.value())
    columns = []
    with open(UNIFIED_CSV, 'r') as unified:
        reader = csv.reader(unified)
        for line in reader:
            columns = line
            break
    with open(UNIFIED_CSV, 'a+') as indata:
        writer = csv.writer(indata)
        data.update(file_metadata)
        writer.writerow([data.get(col, 0) for col in columns])

if __name__ == "__main__":
    htmls = [html.resolve() for html in RAW_FILES if html.is_file()]
    print("Creando metadata gastos operacionales (json)")
    if not OPERATIONAL_METADATA.is_file():
        write_json(OPERATIONAL_METADATA, operational_metadata(htmls))
    else:
        metadata = []
        with open(OPERATIONAL_METADATA, 'r') as infile:
            metadata = json.load(infile)

    print("Creando metadata archivo gastos operacionales (csv)")
    if not UNIFIED_CSV.is_file():
        with open(OPERATIONAL_METADATA, 'r') as f:
            # print(list(json.load(f)['columns'].values()))
            column_names = list(json.load(f)['columns'].values())
            write_csv_header(UNIFIED_CSV, column_names)

    print("Creando archivo metadata diputados (kkkkkkkkkkkkkkkkkcsv)")    
    metadata =json.load(f)
    with open(METADATA_FILE, 'r') as f:
        metadata = json.load(f)

    print("Creando archivo gastos operacionales (csv)")
    total_files = len(htmls)
    for idx, html in enumerate(htmls):
        file_metadata = filename_metadata(html)
        print(f"Añadidos {idx} de {total_files}")
        data = {}
        with open(html, 'r') as raw_html:
            header, rows = extract_operational_data(raw_html)
            data = dict(zip(header, rows))
            if data:
                write_operational_data(data, file_metadata)


