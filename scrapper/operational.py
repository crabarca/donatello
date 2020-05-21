from selenium import webdriver
from selenium.webdriver.support.ui import Select
from utils import extract_operational_data, table_to_csv
from urls import OPER_URL
from time import sleep

class OperationalDriver:
  def __init__(self, operational_url, reference_data):
    self.operational_url = operational_url
    self.ref_data = reference_data
    self.driver = webdriver.Firefox()
    self.years = ['2019', '2020'] 
    self.months = list(range(1,13))

  def run(self):
    for deputy in self.ref_data:
      deputy_id = self.ref_data[deputy]['internal_id']
      self.driver.get(self.operational_url.format(deputy_id))
      sleep(1)
      for year in self.years:
        for month in self.months:
          monthSelect = Select(self.driver.find_element_by_id('ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlMes'))
          monthSelect.select_by_value(str(month))
          sleep(0.4)
          yearSelect = Select(self.driver.find_element_by_id('ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlAno'))
          yearSelect.select_by_value(str(year))
          sleep(0.4)
          expenses = self.driver.find_element_by_class_name("table-responsive").get_attribute('innerHTML')
          header, row = extract_operational_data(expenses, year, month)
          if header and row:
            table_to_csv(deputy, header,row)
    self.driver.close()