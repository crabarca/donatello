# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from bs4 import BeautifulSoup as Bs
import unicodedata


class DiputadosPipeline:
    def process_item(self, item, spider):
        raw_table = item['data'][0]
        header, row = self.extract_operational_data(raw_table, 2020, 2)
        print(header, row)
        return item

    def extract_operational_data(self, raw_html, year, month):
        """
            Desde los datos raw se extraen las columnas 
        """
        headers, rows = self.extract_table(raw_html)
        if not headers or not rows:
            return [], []

        # Por alguna razon a alguien le parecio una excelente idea
        # dejar una columna extra con espacios en blancos
        clean_rows = [row for row in rows if row != []]
        transposed = [list(row) for row in zip(*clean_rows)]

        # Reemplazar los 223.234 por 223234
        header, row = transposed[0], list(map(lambda s: s.replace('.', ''), transposed[1]))
        header.insert(0, 'ANO')
        header.insert(1, 'MES')
        row.insert(0, year)
        row.insert(1, month)
        return header, row 

    def extract_table(self, raw_html):
        """
            Extrae la información desde la tabla en html 
            Retorna: 
            Tabla con headers y datos en formato lista
        """
        parser = Bs(raw_html, 'html.parser')
        table = parser.find('table', {"class": 'tabla'})
        if table:
            th = table.find_all('th')
            headers = [self.clean_text(header.string) for header in th]
            rows = []
            for row in table.find_all('tr'):
                rows.append([self.clean_text(val.string) for val in row.find_all('td')])
            return headers, rows
        else:
            return [], []


    def clean_text(self, text):
        # Por alguna razon el texto esta bastante sucio  con unicode chars y espacios
        return unicodedata.normalize("NFKD", text).replace('\n', '').strip()