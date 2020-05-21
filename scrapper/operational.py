from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as Bs
from diputados import deputy_ids
from urls import OPER_URL
from time import sleep
import string
import unicodedata

years = ['2019', '2020']
driver = webdriver.Firefox()


def create_expenses_map(html):
  # Create expenses map
  pass

def extract_expenses_table(raw_html):
  def clean_text(text):
    return unicodedata.normalize("NFKD", text).replace('\n', '').strip()

  # Extract table from raw html
  parser = Bs(raw_html, 'html.parser')
  table = parser.find('table', {"class": 'tabla'})
  rows = []
  if table:
    for row in table.find_all('tr'):
      rows.append([clean_text(val.string) for val in row.find_all('td')][:2])
      # rows.append([val.string.encode('utf-8') for val in row.find_all('td')])
    # print(table)
  else:
    print("No hay datos para este mes")

  print(rows) 

if __name__ == "__main__":
  for deputy in deputy_ids:
    driver.get(OPER_URL.format(deputy))
    sleep(1)
    for year in years:
      for month in list(map(str, range(1,4))):
        monthSelect = Select(driver.find_element_by_id('ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlMes'))
        monthSelect.select_by_value(month)
        sleep(0.2)
        yearSelect = Select(driver.find_element_by_id('ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlAno'))
        yearSelect.select_by_value(year)
        sleep(0.2)
        expenses = driver.find_element_by_class_name("table-responsive").get_attribute('innerHTML')
        extract_expenses_table(expenses)
        
driver.close()