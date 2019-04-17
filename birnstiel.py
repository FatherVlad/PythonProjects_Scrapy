# -*- coding: utf-8 -*-
import scrapy
import re 
from landlord.items.aditem import AdItem
from tools.transformerTool import TransformerTool
from landlord.items.aditem import AdItem


class BirnstielSpider(scrapy.Spider):
	name = 'birnstiel'
	allowed_domains = ['www.birnstiel-immobilien.de']
	start_urls = ['https://www.birnstiel-immobilien.de/Immobilienangebote-6-Lokal-Wohnimmobilien/Wohnen-Miete.php']

	def parse(self, response):
		for url in response.xpath("//div[@class='listen-details']/a/@href").extract():
			url = url.replace('..','')
			abs_url = 'http://www.birnstiel-immobilien.de'+url
			yield scrapy.Request(abs_url, callback=self.detail_page, dont_filter=True)
	#	next_page  = response.xpath("//a[i[@class='ion-ios-arrow-right']]/@href").extract_first()
	#	if next_page:
	#		abs_next_page = next_page
	#		yield scrapy.Request(abs_next_page, dont_filter=True)
	
	
	def detail_page(self,response):
		description = response.xpath("//div[@class='detailTxt']/p/text()").extract()
		monthly_rent = response.xpath("//td[text()='Preis:']//following::td/text()").extract_first().replace(' €','')
		monthly_rent_extra_costs = response.xpath("//td[text()='Nebenkosten:']//following::td/text()").extract_first().replace(' €','')
		monthly_rent_total = int(monthly_rent)+int(monthly_rent_extra_costs)
		images = []
	 
		for img in response.xpath("//div[@class='bilddiv']/a/@href").extract():
			img  = 'http://www.birnstiel-immobilien.de'+img.replace('..','')
			images.append(img)

		aditem = AdItem(source = self.name,
			title = response.xpath("//h1/text()").extract_first(),
			description = description[:2],
			monthly_rent = monthly_rent+' €',
			monthly_rent_extra_costs = monthly_rent_extra_costs+' €' ,
			monthly_rent_total =str(monthly_rent_total)+' €' ,
			rooms = response.xpath("//td[text()='Zimmer:']//following::td/text()").extract_first(),
		#	available_from = response.xpath("//td[text()='Free From']/following::td/text()").extract_first(),
		#	deposit = response.xpath("//td[contains(text(),'Kaution')]/following::td/text()").extract_first(),
			size_m2 = response.xpath("//td[text()='Wohnfläche: ']//following::td/text()").extract_first(),
			category = "rental_apartment",
		#	floor = response.xpath("//td[text()='Etage']/following::td/text()").extract_first(),
			address = response.xpath("//td[text()='Anschrift']//following::td/text()").extract_first().strip(),
			reference_id =response.xpath("//td[text()='Id: ']//following::td/text()").extract_first().strip(),
			detail_url = response.url, 
			images = images,    
			)

		if TransformerTool.validate(aditem):
			yield aditem
