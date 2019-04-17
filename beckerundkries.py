# -*- coding: utf-8 -*-
import scrapy
from landlord.items.aditem import AdItem
from tools.transformerTool import TransformerTool

class BeckerundkriesSpider(scrapy.Spider):
    name = 'beckerundkries'
    allowed_domains = ['www.beckerundkries.de']
    start_urls = ['https://beckerundkries-mietangebote.immomio.de/immobilien/']

    def parse(self, response):
        for url in response.xpath("//h3/a/@href").extract():
            abs_url = url
            yield scrapy.Request(abs_url, callback=self.detail_page, dont_filter=True)
        next_page = response.xpath("//a[@class='next page-numbers']/@href").extract_first()
        if next_page:
            abs_next_page = next_page
            yield scrapy.Request(abs_next_page,dont_filter=True) 

    def detail_page(self,response):

        images = []
     
        for img in response.xpath("//div[@id='immomakler-galleria']//a/@href").extract():
            images.append(img)

           
        aditem = AdItem(source = self.name,
            title = response.xpath("//h1[@class='property-title']/text()").extract_first(),
            monthly_rent = response.xpath("//div[text()='Kaltmiete']//following::div/text()").extract_first(),
            monthly_rent_extra_costs = response.xpath("//div[text()='Nebenkosten']//following::div/text()").extract_first(),
            monthly_rent_total = response.xpath("//div[contains(text(),'Gesamtmiete')]//following::div/text()").extract_first(),
            rooms = response.xpath("//div[text()='Zimmer']//following::div/text()").extract_first(),
            available_from = response.xpath("//div[text()='Verfügbar ab']//following::div/text()").extract_first(),
            deposit = response.xpath("//div[text()='Kaution']//following::div/text()").extract_first(),
            size_m2 = response.xpath("//div[contains(text(),'fläche')]//following::div/text()").extract_first(),
            category = "rental_apartment",
            floor = response.xpath("//div[text()='Etage']//following::div/text()").extract_first(),
            address = response.xpath("//h2[@class='property-subtitle']/text()").extract_first(),
            reference_id = response.xpath("//div[contains(text(),'Objekt ID')]//following::div/text()").extract_first(),
            detail_url = response.url, 
            images = images,    
            )

        if TransformerTool.validate(aditem):
            yield aditem   