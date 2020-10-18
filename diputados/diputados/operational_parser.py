from bs4 import BeautifulSoup as Bs
import logging
import unicodedata


RAW_HTML = "../../data/Honorable Cámara de Diputadas y Diputados - Chile.html"

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

def parse_year(raw_html):
    parser = Bs(raw_html, 'html.parser')
    selector = parser.select("#ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlAno > option[selected='selected']")
    return selector[0].text

def parse_month(raw_html):
    parser = Bs(raw_html, 'html.parser')
    selector = parser.select("#ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlMes > option[selected='selected']")
    return selector[0].text

def clean_text(text):
    # Por alguna razon el texto esta bastante sucio  con unicode chars y espacios
    return unicodedata.normalize("NFKD", text).replace('\n', '').strip()

if __name__ == "__main__":
    raw_html = open(RAW_HTML)
    year = parse_year(raw_html)
    raw_html = open(RAW_HTML)
    month = parse_month(raw_html)
    raw_html = open(RAW_HTML)
    header, rows = extract_operational_data(raw_html)
    print(header, rows)

