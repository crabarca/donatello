from urls import BASE_URL, PROFILE_URL
from bs4 import BeautifulSoup as Bs

import urllib.parse as urlparse
from urllib.parse import parse_qs

import requests as rq

class Parser:
  def __init__(self, base_url):
    self.base_url = BASE_URL
    self.details_url = PROFILE_URL

  def base_site_request(self):
    r = rq.get(self.base_url)
    if r.status_code == 200:
      return r.text

  def deputy_details_request(self, uid):
    r = rq.get(self.details_url.format(uid))
    if r.status_code == 200:
      return r.text

  def _extract_deputy_id(self, url):
    parsed = urlparse.urlparse(url)
    return parse_qs(parsed.query)['prmID'][0]

  def get_deputy_reference_data(self):
    base_html = self.base_site_request()
    parser = Bs(base_html, 'html.parser')
    deputies = parser.find_all('article', 'grid-2')
    data = {}
    for deputy in deputies:
      name = deputy.h4.string.split(".")[1].strip(" ")
      url = deputy.a['href']
      internal_id = self._extract_deputy_id(url)
      data[name] = {'url': url, 'internal_id': internal_id}
    return data

  def get_deputy_details(uid):
    base_html = Parser.deputy_details_request(uid)
    parser = Bs(base_html, 'html.parser')
    p_tag = parser.find('section', {'id': 'info-ficha'}) 
    profile = profile_section.findChildren('p', recursive=True)
    data = profile

