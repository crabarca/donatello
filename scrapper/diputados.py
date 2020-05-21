from urls import BASE_URL
from bs4 import BeautifulSoup as Bs

import urllib.parse as urlparse
from urllib.parse import parse_qs

import requests as rq


def base_site_request(base_url):
  response = rq.get(base_url)
  return response.text

def deputy_sites_urls(base_html):
  parser = Bs(base_html, 'html.parser')
  deputies = parser.find_all('article', 'grid-2')
  deputy_urls = []
  for deputy in deputies:
    deputy_urls.append(deputy.a['href'])
  return deputy_urls

def deputy_names(base_html):
  parser = Bs(base_html, 'html.parser')
  deputies = parser.find_all('article', 'grid-2')
  name_list  = []
  for deputy in deputies:
    name_list.append(deputy.h4.string.split(".")[1].strip(" "))
  return name_list

def deputy_ids(deputy_urls):
  ids = []
  for url in deputy_urls:
    parsed = urlparse.urlparse(url)
    ids.append(parse_qs(parsed.query)['prmID'][0])
  return ids

base_html = base_site_request(BASE_URL)
deputy_names = deputy_names(base_html) 
deputy_urls = deputy_sites_urls(base_html)
deputy_ids = deputy_ids(deputy_urls)

if __name__ == "__main__":
  base_html = base_site_request(BASE_URL)
  deputy_names = deputy_names(base_html) 
  deputy_urls = deputy_sites_urls(base_html)
  deputy_ids = deputy_ids(deputy_urls)
  print("holaa")




