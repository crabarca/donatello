from django.core.management.base import BaseCommand
from RiegaMeApp.models import Plant
from bs4 import BeautifulSoup as Bs

import random
import requests
import json

class Command(BaseCommand):
    help = 'Populate db based on the open data endpoint by the www.camara.cl'

  def handle(self, *args, **options):
      run_seed(self)

def clear_data():
    Plant.objects.all().delete()
    
def getPlantToken():
    url = 'http://trefle.io/api/auth/claim?token=dS9yWm5mYmFIR1EyNm9uYkluUlVUdz09&origin=localhost:8080'
    response = requests.post(url, data = {})
    print(response)
    return response.json()
    
    
def create_plant_for_library(info):
    plant = Plant(
        plant_name = info["common_name"],
        stats = f'Growth rate: { info["main_species"]["specifications"]["growth_rate"] }. Duration: { info["main_species"]["duration"] }',
        properties = f'{ info["main_species"]["specifications"]["growth_habit"] }',
        specifications = (
            f'It grows better at { info["main_species"]["specifications"]["growth_period"] }.'
            f'Bloom period: { info["main_species"]["seed"]["bloom_period"] }.'
            f'Foliage: { info["main_species"]["foliage"]["color"] }.'
            f'Max Mature Height: {round(info["main_species"]["specifications"]["mature_height"]["cm"], 2)}'
        ),
        dificulty = random.randint(0,5),
        popularity = random.randint(0,5)
    )
    plant.save()
    return plant

def run_seed(self):
    clear_data()
    
    trefle_token = getPlantToken()["token"]
    url = 'https://trefle.io/api/plants?complete_data=true&token=' + trefle_token
    trefle_plants = requests.get(url = url, params = {}).json()
    
    for plant in trefle_plants:
        
        single_url = f'https://trefle.io/api/plants/{ plant["id"] }?token=' + trefle_token
        plant_info = requests.get(url = single_url, params = {}).json()
        if plant_info["class"]:
            create_plant_for_library(plant_info)