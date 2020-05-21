from urls import BASE_URL, OPER_URL
from operational import OperationalDriver
from parser import Parser


if __name__ == "__main__":

  parser = Parser(BASE_URL)  
  reference_data = parser.get_deputy_reference_data()
  operationalDriver = OperationalDriver(OPER_URL, reference_data)
  operationalDriver.run()






