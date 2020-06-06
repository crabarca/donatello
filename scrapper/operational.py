from selenium import webdriver
from selenium.webdriver.support.ui import Select
from utils import extract_operational_data, table_to_csv
from urls import OPER_URL
from time import sleep
import csv

class OperationalDriver:
  def __init__(self, operational_url, reference_data):
    self.operational_url = operational_url
    self.ref_data = reference_data
    self.driver = webdriver.Firefox()
    self.years = ['2019', '2020'] 
    self.months = list(range(1,13))


  def scrap_by_date(self, deputy_id, year, month):
    self.driver.get(self.operational_url.format(deputy_id))
    sleep(0.3)
    try:
      monthSelect = Select(self.driver.find_element_by_id('ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlMes'))
      monthSelect.select_by_value(str(month))
      sleep(0.2)
      yearSelect = Select(self.driver.find_element_by_id('ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlAno'))
      yearSelect.select_by_value(str(year))
      sleep(0.2)
      expenses = self.driver.find_element_by_class_name("table-responsive").get_attribute('innerHTML')
    except:
      return False

    header, row = extract_operational_data(expenses, year, month)
    deputy_name = [dep for dep in self.ref_data if self.ref_data[dep]['internal_id'] == deputy_id][0]
    if header and row:
      # Agregar data solamente si existe, la tabla puede estar vacia
      table_to_csv(deputy_name, header,row)
      return True
    

  def write_log(self, deputy, year, month):
    """
      Escribe un archivo de log rudimentario para saber que data ya existe
    """
    with open('/home/cristobal/repos2/donatello/scrapper/log.txt', 'a+') as f:
      f.write(f"{deputy}_{year}_{month}\n")

  def read_log(self, filepath):
    with open(filepath, 'r') as f:
      lines = [line.strip() for line in f.readlines()]
      return lines

  def run_2(self):
    scrapped = self.read_log('/home/cristobal/repos2/donatello/scrapper/log.txt') 
    for deputy in self.ref_data:
      deputy_id = self.ref_data[deputy]['internal_id']
      for year in self.years:
        for month in self.months:
          # Evita scrapear si ya existe la data
          if f"{deputy}_{year}_{month}" not in scrapped:
            if self.scrap_by_date(deputy_id, year, month):
              self.write_log(deputy, year, month)
          else:
            continue