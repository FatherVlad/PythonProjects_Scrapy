# -*- coding: utf-8 -*-
import scrapy
import re 
from landlord.items.aditem import AdItem
from tools.transformerTool import TransformerTool
from landlord.items.aditem import AdItem


class ArtesiaSpider(scrapy.Spider):
	name = 'artesia'
	allowed_domains = ['www.artesia-immobilien.de']
	start_urls = ['https://artesia-immobilien.de/mieten/miet-angebote/']
	def parse(self, response):
		for url in response.xpath("//div[@class='property-name']/a/@href").extract():
			abs_url = url
			yield scrapy.Request(abs_url, callback=self.detail_page, dont_filter=True)
	#	next_page  = response.xpath("//a[i[@class='ion-ios-arrow-right']]/@href").extract_first()
	#	if next_page:
	#		abs_next_page = next_page
	#		yield scrapy.Request(abs_next_page, dont_filter=True)    


	def detail_page(self,response):
		title = response.xpath("//title/text()").extract_first()
		monthly_rent_extra_costs = response.xpath("//div[text()='Nebenkosten:']//following::div[@class='artesia-value']/text()").extract_first()
		title = title.replace("- Artesia","")
		if monthly_rent_extra_costs is None:
				monthly_rent_extra_costs ="0"	
		images = []
	 
		for img in  response.xpath("//a[contains(@href,'.png')]/@href").extract():
			images.append(img)

		aditem = AdItem(source = self.name,
			title = title,
			description = response.xpath("//h3[text()='Lagebeschreibung']//following::p/span/text()").extract_first(),
			monthly_rent = response.xpath("//div[text()='Kaltmiete:']//following::div[@class='artesia-value']/text()").extract_first(),
			monthly_rent_extra_costs = monthly_rent_extra_costs,
			monthly_rent_total = response.xpath("//div[text()='Gesamtmiete:']//following::div[@class='artesia-value']/text()").extract_first(),
			rooms = response.xpath("//div[text()='Zimmer:']//following::div[@class='artesia-value']/text()").extract_first(),
			available_from = response.xpath("//div[text()='Verfügbarkeit:']//following::div[@class='artesia-value']/text()").extract_first(),
		#	deposit = response.xpath("//td[contains(text(),'Kaution')]/following::td/text()").extract_first(),
			size_m2 = response.xpath("//div[text()='Wohnfläche:']//following::div[@class='artesia-value']/text()").extract_first(),
			category = "rental_apartment",
		#	floor = response.xpath("//td[text()='Etage']/following::td/text()").extract_first(),
			address = "Berlin",
		#	reference_id =response.xpath("//td[text()='Kennung']/following::td/text()").extract_first().strip(),
			detail_url = response.url, 
			images = images,    
			)

		if TransformerTool.validate(aditem):
			yield aditem   

  
