# -*- coding: utf-8 -*-
import scrapy
import re 
from landlord.items.aditem import AdItem
from tools.transformerTool import TransformerTool
from landlord.items.aditem import AdItem


class AvialSpider(scrapy.Spider):
	name = 'avial'
	allowed_domains = ['www.avial.com']
	start_urls = ['https://www.avial.com/immobilien/?post_type=immomakler_object&nutzungsart%5B0%5D=wohnen&typ%5B0%5D=wohnung&center&radius=1&objekt-id&collapse&von-qm=0.00&bis-qm=305.00&von-zimmer=0.00&bis-zimmer=7.00&von-kaltmiete=0.00&bis-kaltmiete=520100.00&von-kaufpreis=0.00&bis-kaufpreis=6025000.00#038;nutzungsart%5B0%5D=wohnen&typ%5B0%5D=wohnung&center&radius=1&objekt-id&collapse&von-qm=0.00&bis-qm=305.00&von-zimmer=0.00&bis-zimmer=7.00&von-kaltmiete=0.00&bis-kaltmiete=520100.00&von-kaufpreis=0.00&bis-kaufpreis=6025000.00']

	def parse(self, response):
		for url in response.xpath("//h3[@class='property-title']/a/@href").extract():
		#	type_check = url.xpath("//h3/a/@href").extract_first()
		#	if "wohnung" or "wohnen" in type_check:
			abs_url = url
			yield scrapy.Request(abs_url, callback=self.detail_page, dont_filter=True)
		next_page = response.xpath("//a[@class='next page-numbers']/@href").extract_first()
		if next_page:
			abs_next_page = next_page
			yield scrapy.Request(abs_next_page,dont_filter=True) 

	def detail_page(self,response):

		monthly_rent = response.xpath("//div[text()='Kaltmiete']/following-sibling::div/text()").extract_first()
		monthly_rent_total = response.xpath("//div[text()='Warmmiete']/following-sibling::div/text()").extract_first()
		if monthly_rent is None:
			monthly_rent = monthly_rent_total


		images = []
	 
		for img in response.xpath("//div[@id='immomakler-galleria']//a/@href").extract():
			images.append(img)

		   

		aditem = AdItem(source = self.name,
			title =  response.xpath("//h1[@class='property-title']/text()").extract_first(),
			description = response.xpath("//h3/following-sibling::p/text()").extract_first(),
			monthly_rent = monthly_rent,
		#	monthly_rent_extra_costs = response.xpath("//dt[text()='Betriebskosten']//following::dd/p/text()").extract_first(),
			monthly_rent_total = monthly_rent_total,
			rooms = response.xpath("//div[text()='Zimmer']/following-sibling::div/text()").extract_first()+" Zimmer",
			available_from = response.xpath("//div[text()='Verfügbar ab']/following-sibling::div/text()").extract_first(),
			deposit = response.xpath("//div[text()='Kaution']/following-sibling::div/text()").extract_first(),
			size_m2 = response.xpath("//div[contains(text(),'fläche')]/following-sibling::div/text()").extract_first(),
			category = "rental_apartment",
			floor = response.xpath("//div[text()='Etage']/following-sibling::div/text()").extract_first(),
			address = response.xpath("//h2[@class='property-subtitle']/text()").extract_first(),
			reference_id = response.xpath("//div[contains(text(),'ID')]/following-sibling::div/text()").extract_first(),
			detail_url = response.url, 
			images = images,    
			)

		if TransformerTool.validate(aditem):
			yield aditem   
