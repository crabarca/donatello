from urls import BASE_URL
from bs4 import BeautifulSoup as Bs

import urllib.parse as urlparse
from urllib.parse import parse_qs

import requests as rq

class Parser:
  def __init__(self, base_url):
    self.base_url = base_url

  def _base_site_request(self):
    return rq.get(self.base_url).text

  def _extract_deputy_name(self, bstring):
    return bstring.h4.string.split(".")[1].strip(" ")
  
  def _extract_deputy_url(self, bstring):
    return bstring.a['href']
  
  def _extract_deputy_id(self, url):
    parsed = urlparse.urlparse(url)
    return parse_qs(parsed.query)['prmID'][0]

  def get_deputy_reference_data(self):
    base_html = self._base_site_request()
    parser = Bs(base_html, 'html.parser')
    deputies = parser.find_all('article', 'grid-2')
    data = {}
    for deputy in deputies:
      name = self._extract_deputy_name(deputy)
      url = self._extract_deputy_url(deputy)
      internal_id = self._extract_deputy_id(url)
      data[name] = {'url': url, 'internal_id': internal_id}
    return data

  def get_deputy_profile(self):
    base_html = self.