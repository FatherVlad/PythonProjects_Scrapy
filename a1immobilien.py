# -*- coding: utf-8 -*-
import scrapy
import re 
from landlord.items.aditem import AdItem
from tools.transformerTool import TransformerTool
from landlord.items.aditem import AdItem


class A1immobilienSpider(scrapy.Spider):
    name = 'a1immobilien'
    allowed_domains = ['www.a1immobilien.de']
    start_urls = ['http://www.a1immobilien.de/wohnungen/zimmer/1','http://www.a1immobilien.de/wohnungen/zimmer/4']


    def parse(self, response):
        for url in response.xpath("//h5/a/@href").extract():
            abs_url = 'http://www.a1immobilien.de'+ url
            yield scrapy.Request(abs_url, callback=self.detail_page, dont_filter=True)
        #   next_page  = response.xpath("//a[i[@class='ion-ios-arrow-right']]/@href").extract_first()
        #   if next_page:
        #          abs_next_page = next_page
        #          yield scrapy.Request(abs_next_page, dont_filter=True)


    def detail_page(self,response):

       	images = []
         
        for img in response.xpath("//div[@class='item']//img[contains(@src,'.JPG')]/@src").extract():
            img = 'http://www.a1immobilien.de' + img
            images.append(img)

       	aditem = AdItem(source = self.name,
                title = response.xpath("//h2/text()").extract_first().strip(),
                #description = description + location,
                monthly_rent = response.xpath("//td/b[text()='Kaltmiete:']//following::td/text()").extract_first(),
                monthly_rent_extra_costs = response.xpath("//td/b[text()='Nebenkosten:']//following::td/text()").extract_first(),
                monthly_rent_total = response.xpath("//td/b[text()='Warmmiete:']//following::td/text()").extract_first(),
                rooms = response.xpath("//td/b[text()='Zimmer:']//following::td/text()").extract_first().replace('.00',''),
                available_from = response.xpath("//td/b[text()='Bezug ab:']//following::td/text()").extract_first(),
                deposit = response.xpath("//td/b[text()='Kaution:']//following::td/text()").extract_first(),
                size_m2 = response.xpath("//td/b[text()='Wohnfläche:']//following::td/text()").extract_first(),
                category = "rental_apartment",
                floor = response.xpath("//td/b[text()='Etage:']//following::td/text()").extract_first(),
                address = response.xpath("//td/b[text()='Lage:']//following::td/text()").extract_first().strip(),
                #reference_id =response.xpath("//td[text()='Kennung']/following::td/text()").extract_first().strip(),
                detail_url = response.url, 
                images = images,    
               )

        if TransformerTool.validate(aditem):
        	    yield aditem   
