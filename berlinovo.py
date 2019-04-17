# -*- coding: utf-8 -*-
import scrapy
import re 
from landlord.items.aditem import AdItem
from tools.transformerTool import TransformerTool
from landlord.items.aditem import AdItem


class BerlinovoSpider(scrapy.Spider):
	name = 'berlinovo'
	allowed_domains = ['www.berlinovo.de']
	start_urls = ['https://www.berlinovo.de/de/suche-wohnungen?']
	

	def parse(self, response):
		for url in response.xpath("//div[@class='views-field views-field-title']/span[@class='field-content']/a/@href").extract():
		#	type_check = url.xpath("//h3/a/@href").extract_first()
		#	if "wohnung" or "wohnen" in type_check:
			urls = "https://www.berlinovo.de"
			abs_url = urls+url
			yield scrapy.Request(abs_url, callback=self.detail_page, dont_filter=True)
	#	next_page = response.xpath("//li[@class='nav-next']/a/@href").extract_first()
	#	if next_page:
	#		abs_next_page = next_page
	#		yield scrapy.Request(abs_next_page,dont_filter=True) 

	def detail_page(self,response):

	#	description = "".join(response.xpath('//div[@class="tab-content"]/div[1]/p/text()').extract())
	#	location = "".join(response.xpath('//div[@class="tab-content"]/div[3]/p/text()').extract())
	#	ref_id = response.xpath("//i[@class='obdt-id-text']/text()").extract_first()
		address = response.xpath("//span[contains(text(),'Adresse:')]//following::div/span[@class='address']/text()").extract()
	#	address = address.replace("Etagenwohnung -  -",'')
		images = []
	 
		for img in response.xpath("//ul/li/a[contains(@href, '.jpg')]/@href").extract():
			images.append(img)

		   

		aditem = AdItem(source = self.name,
			title =  response.xpath("//h1[@class='title']/text()").extract_first().strip(),
			description = response.xpath("//div[contains(text(),'Lageinformationen:')]//following::div[@class='field-items']/div/text()").extract_first(),
			monthly_rent = response.xpath("//span[contains(text(),'Kaltmiete:')]//following::span/text()").extract_first(),
		#	monthly_rent_extra_costs = response.xpath("//dt[text()='Betriebskosten']//following::dd/p/text()").extract_first(),
			monthly_rent_total = response.xpath("//span[contains(text(),'Warmmiete:')]//following::span/text()").extract_first(),
			rooms = response.xpath("//span[contains(text(),'Zimmer:')]//following::span/text()").extract_first()+" Zimmer",
			available_from = response.xpath("//span[contains(text(),'Verfügbar ab')]//following::span/text()").extract_first(),
			deposit = response.xpath("//span[contains(text(),'Kautionsbetrag:')]//following::span/text()").extract_first(),
			size_m2 = response.xpath("//span[contains(text(),'fläche:')]//following::span/text()").extract_first(),
			category = "rental_apartment",
			floor = response.xpath("//span[text()='Etage: ']//following::span/text()").extract_first(),
			address = address[1].strip()+" "+address[0].strip(),
			reference_id = response.xpath("//span[@class='label']//following::span/text()").extract_first(),
			detail_url = response.url, 
			images = images,    
			)

		if TransformerTool.validate(aditem):
			yield aditem   
