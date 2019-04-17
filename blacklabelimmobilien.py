# -*- coding: utf-8 -*-
import scrapy
import re 
from landlord.items.aditem import AdItem
from tools.transformerTool import TransformerTool
from landlord.items.aditem import AdItem

class BlacklabelimmobilienSpider(scrapy.Spider):
    name = 'blacklabelimmobilien'
    allowed_domains = ['www.blacklabelimmobilien.de']
    start_urls = ['https://blacklabelimmobilien.de/properties/?post_type=immomakler_object&vermarktungsart%5B%5D=miete&objekt-id=&collapse=+in&von-qm=0.00&bis-qm=710.00&von-zimmer=0.00&bis-zimmer=12.00&von-kaufpreis=0.00&bis-kaufpreis=4925000.00']

    
    def parse(self, response):
        for url in response.xpath("//h3/a/@href").extract():
            abs_url = url
            yield scrapy.Request(abs_url, callback=self.detail_page, dont_filter=True) 


    def detail_page(self,response):
        images = []
     
        for img in response.xpath("//a[contains(@href,'.jpg')]/@href").extract():
            images.append(img)

        aditem = AdItem(source = self.name,
            title = response.xpath("//h2/text()").extract_first(),
            description = response.xpath("//h3[text()='Beschreibung']//following::p/text()").extract_first(),
            monthly_rent = response.xpath("//div[contains(text(),'Kaltmiete')]/following-sibling::div/text()").extract_first(),
            monthly_rent_extra_costs = response.xpath("//div[contains(text(),'Betriebskosten ')]/following-sibling::div/text()").extract_first(),
            monthly_rent_total = response.xpath("//div[contains(text(),'Gesamtbelastung ')]/following-sibling::div/text()").extract_first(),
            rooms = response.xpath("//div[text()='Zimmer']/following-sibling::div/text()").extract_first(),
            available_from = response.xpath("//div[text()='Verfügbar ab']/following-sibling::div/text()").extract_first(),
            deposit = response.xpath("//div[text()='Kaution']/following-sibling::div/text()").extract_first(),
            size_m2 = response.xpath("//div[contains(text(),'Wohnfläche')]/following-sibling::div/text()").extract_first(),
            category = "rental_apartment",
        #   floor = response.xpath("//td[text()='Etage']/following::td/text()").extract_first(),
            address = response.xpath("//h3/text()").extract_first(),
            reference_id =response.xpath("//div[contains(text(),'Objekt ID')]/following::div/text()").extract_first().strip(),
            detail_url = response.url, 
            images = images,    
            )

        if TransformerTool.validate(aditem):
            yield aditem   
