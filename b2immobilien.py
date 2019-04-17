# -*- coding: utf-8 -*-
import scrapy
import re 
from landlord.items.aditem import AdItem
from tools.transformerTool import TransformerTool
from landlord.items.aditem import AdItem


class B2immobilienSpider(scrapy.Spider):
	name = 'b2immobilien'
	allowed_domains = ['www.b2immobilien.de']
	start_urls = ['https://b2immobilien.de/immobilien/?typefilter=1AB70647-4B47-41E2-9571-CA1CA16E0308%7C0']

	def parse(self, response):
		for url in response.xpath("//div[@class='estate_list']/div/a/@href").extract():
			abs_url = url
			yield scrapy.Request(abs_url, callback=self.detail_page, dont_filter=True)
		next_page  = response.xpath("//a[i[@class='ion-ios-arrow-right']]/@href").extract_first()
		if next_page:
			abs_next_page = next_page
			yield scrapy.Request(abs_next_page, dont_filter=True)    


	def detail_page(self,response):

		images = []
	 
		for img in response.xpath("//div/@data-image-size-tall").extract():
			img = img.replace("//","")
			images.append(img)

		aditem = AdItem(source = self.name,
			title = response.xpath("//h1/text()").extract_first().strip(),
		#	description = description + location,
			monthly_rent = response.xpath("//td[contains(text(),'Miete')]/following::td/text()").extract_first(),
			monthly_rent_extra_costs = response.xpath("//td[contains(text(),'Nebenkosten')]/following::td/text()").extract_first(),
			monthly_rent_total = response.xpath("//td[contains(text(),'Warmmiete')]/following::td/text()").extract_first(),
			rooms = response.xpath("//td[contains(text(),'Zimmer')]/following::td/text()").extract_first(),
		#	available_from = response.xpath("//td[text()='Free From']/following::td/text()").extract_first(),
			deposit = response.xpath("//td[contains(text(),'Kaution')]/following::td/text()").extract_first(),
			size_m2 = response.xpath("//td[contains(text(),'fläche')]/following::td/text()").extract_first(),
			category = "rental_apartment",
			floor = response.xpath("//td[text()='Etage']/following::td/text()").extract_first(),
			address = response.xpath("//td[text()='Lage']/following::td/text()").extract_first().strip(),
			reference_id =response.xpath("//td[text()='Kennung']/following::td/text()").extract_first().strip(),
			detail_url = response.url, 
			images = images,    
			)

		if TransformerTool.validate(aditem):
			yield aditem   

   
