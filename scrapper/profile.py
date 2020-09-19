from utils import extract_profile
from urls import PROFILE_URL
from parser import Parser
import requests as rq

class Profile:
  def __init__(self, reference_data):
    self.ref_data = reference_data

  def run(self):
    for deputy in self.ref_data:
      internal_id = self.ref_data[deputy]['internal_id']
      data = Parser.get_deputy_details(internal_id) 
      response = rq.get(PROFILE_URL.format(internal_id))

      profile = extract_profile(response.text)

