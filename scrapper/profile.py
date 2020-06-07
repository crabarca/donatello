from utils import extract_profile

import request as rq

class Profile:
  def __init__(self, reference_data):
    self.ref_data = reference_data

  def run(self):
    for deputy in self.ref_data:
      raw_html = rq.get(self.ref_data[deputy]['url'])
      profile = extract_profile(raw_html)
