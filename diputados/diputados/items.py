# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DiputadosItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Operational(scrapy.Item):
    diputadoId = scrapy.Field()
    year = scrapy.Field()
    month = scrapy.Field()
    data = scrapy.Field()
