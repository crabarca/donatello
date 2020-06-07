from urls import BASE_URL, OPER_URL, PROFILE_URL
from operational import OperationalDriver
from profile import Profile
from parser import Parser


def run_operational(reference_data):
  if reference_data:
    operationalDriver = OperationalDriver(OPER_URL, reference_data)
    operationalDriver.run()


def run_profiles(reference_data):
  if reference_data:
    profileDriver = Profile(reference_data)
    profileDriver.run()

if __name__ == "__main__":
  parser = Parser(BASE_URL)  
  reference_data = parser.get_deputy_reference_data()

  modes = {
    'operational': run_operational,
    'profiles': run_profiles
  } 
  mode = 'profiles'
  # Run mode
  modes[mode](reference_data)









