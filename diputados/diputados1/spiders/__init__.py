# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.


from scrapy.spiders import CrawlSpider, Spider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request, FormRequest
    
class SpiderSp(Spider):
	name = "diputado"
	start_urls = ['http://www.camara.cl/diputados/diputados.aspx']
	def parse(self, response):
		xp = '//article[@class = "grid-2"]/h4/a/@href'
		for url in response.xpath(xp).extract():
			yield (Request('https://www.camara.cl/diputados/' + url, callback=self.parse_manga_list_page))

	def parse_manga_list_page(self, response):
		xp_form = '//*[@id="menu-acordeon"]/li[3]/ul/li[1]/a/@href'
		for url in response.xpath(xp_form).extract():
			yield (Request('https://www.camara.cl/diputados/detalle/'+url, callback=self.parse_box))

	def parse_box(self, response):
		req = Request(response.url,
		                    method='POST',
		                    #body='{"filters": []}',
		                    headers={"Accept": "*/*","Accept-Encoding": "gzip, deflate, br", "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
		                	"Cache-Control": "no-cache" , "Connection": "keep-alive","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
							"Cookie": "_ga=GA1.2.1964487235.1594267649; _gid=GA1.2.615547272.1594267649; _gat=1",
							"Host": "www.camara.cl",
							"Origin": "https://www.camara.cl",
							"Referer": "https://www.camara.cl/diputados/detalle/gastosoperacionales.aspx?prmId=1020",
							"Sec-Fetch-Dest": "empty",
							"Sec-Fetch-Mode": "cors",
							"Sec-Fetch-Site": "same-origin",
							"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
							"X-MicrosoftAjax": "Delta=true",
							"X-Requested-With": "XMLHttpRequest"}, callback=self.parse)
		print('req')
		print(req)
		yield req
