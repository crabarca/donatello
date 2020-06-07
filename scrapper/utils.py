import unicodedata
import csv
from bs4 import BeautifulSoup as Bs
from pathlib import Path


def clean_text(text):
  # Por alguna razon el texto esta bastante sucio  con unicode chars y espacios
  return unicodedata.normalize("NFKD", text).replace('\n', '').strip()

def extract_profile(raw_html):
  parser = Bs(raw_html, 'html.parser')
  profile_section = parser.find('section', {'id': 'info-ficha'})
  profile = profile_section.findChildren('p', recursive=True)
  return profile
    



def extract_operational_data(raw_html, year, month):
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
  header.insert(0, 'Ano')
  header.insert(1, 'Mes')
  row.insert(0, year)
  row.insert(1, month)
  return header, row 

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