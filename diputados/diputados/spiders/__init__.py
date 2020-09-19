# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from scrapy.spiders import CrawlSpider, Spider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy import Request, FormRequest
from diputados.items import Operational
from time import sleep
    
class SpiderSp(Spider):
	name = "diputado"
	start_urls = ['http://www.camara.cl/diputados/diputados.aspx']

	def parse(self, response):
		xp = '//article[@class = "grid-2"]/h4/a/@href'
		diputadoDetailUrls = response.xpath(xp).extract()
		for url in diputadoDetailUrls[:2]:
			yield (Request('https://www.camara.cl/diputados/' + url, callback=self.parse_menu_list_page))

	def parse_menu_list_page(self, response):
		xp = '//*[@id="menu-acordeon"]/li[3]/ul/li[1]/a/@href'
		operacionalUrl = response.xpath(xp).extract()[:2]
		for url in operacionalUrl:
			yield (Request('https://www.camara.cl/diputados/detalle/'+url, callback=self.parse_operational_table))

	def parse_operational_table(self, response):
		diputadoId = response.url.split("prmId=")[1]
		validationXp = '//*[@id="__EVENTVALIDATION"]/@value'
		viewStateXp = '//*[@id="__VIEWSTATE"]/@value'
		viewStateGeneratorXp = '//*[@id="__VIEWSTATEGENERATOR"]/@value'

		eventValidation = response.xpath(validationXp).extract()[0]
		viewState = response.xpath(viewStateXp).extract()[0]
		viewStateGenerator = response.xpath(viewStateGeneratorXp).extract()[0]

		for mes in range(1,3):
			req = FormRequest(response.url,
				method='POST',
				headers={
				"Accept": "*/*","Accept-Encoding": "gzip, deflate, br", 
				"Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
				"Cache-Control": "no-cache" , "Connection": "keep-alive",
				"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
				"Cookie": "_ga=GA1.2.1964487235.1594267649; _gid=GA1.2.615547272.1594267649; _gat=1",
				"Host": "www.camara.cl",
				"Origin": "https://www.camara.cl",
				"Sec-Fetch-Dest": "empty",
				"Sec-Fetch-Mode": "cors",
				"Sec-Fetch-Site": "same-origin",
				"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
				"X-MicrosoftAjax": "Delta=true",
				"X-Requested-With": "XMLHttpRequest"
				}, 
				formdata = {
				"ctl00$ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$ScriptManager1":"ctl00$ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$DetallePlaceHolder$UpdatePanel1|ctl00$ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$DetallePlaceHolder$ddlMes",
				"ctl00$ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$ddlDiputados": str(diputadoId),
				"ctl00$ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$DetallePlaceHolder$ddlMes": str(mes),
				"ctl00$ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$DetallePlaceHolder$ddlAno": "2019",
				"__EVENTTARGET":"ctl00$ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$DetallePlaceHolder$ddlMes",
				"__EVENTARGUMENT":"",
				"__VIEWSTATEGENERATOR": str(viewStateGenerator),
				"__VIEWSTATE": str(viewState),
				"__LASTFOCUS":"",
				"__EVENTVALIDATION": str(eventValidation),
				},
				callback=self.parse_table)
			yield req

	def parse_table(self, response):
		operational = Operational()
		operational['diputadoId'] = response.url.split("prmId=")[1]
		operational['month'] = response.css('#ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlMes') .extract()
		operational['year'] = response.css('#ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlAno').extract()
		# operational['year'] = response.xpath('//*[@id="ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlAno"]/input[@selected="selected")').extract()
		operational['data'] = response.css('.table-responsive').extract()
		yield operational
