# -*- coding: utf-8 -*-
import scrapy
import re 
from landlord.items.aditem import AdItem
from tools.transformerTool import TransformerTool
from landlord.items.aditem import AdItem

class BerlinhomesinSpider(scrapy.Spider):
    name = 'berlinhomesin'
    allowed_domains = ['www.in-berlinhomes.com']
    start_urls = ['http://www.in-berlinhomes.com/']

    def start_requests(self):
        url = "https://www.in-berlinhomes.com/search/"
        body = 'movein=&moveInSearch=&Persons=all&rooms=all&rooms-all=rooms-all&room1=1&room2=2&room3=3&room4=4&sizeFrom=&sizeTo=&From=&To=&Neighborhood=all-active&all-active=all-active&Alt-Treptow=Alt-Treptow&Charlottenburg=Charlottenburg&Friedrichshain=Friedrichshain&Kreuzberg=Kreuzberg&Moabit=Moabit&Neuk%C3%B6lln=Neuk%C3%B6lln&Prenzlauer-Berg=Prenzlauer-Berg&Sch%C3%B6neberg=Sch%C3%B6neberg&Wedding=Wedding&Floor=All&All=All&buy_car_submit=Search+Now'
        yield scrapy.Request(
            url=url,
            body=body,
            method='POST',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            callback=self.parse,
            dont_filter=True,
            meta={'dont_merge_cookies': True}
        )

    def parse(self, response):
        for url in response.xpath("//a[@class='car_name']/@href").extract():
            abs_url = url
            yield scrapy.Request(abs_url, callback=self.detail_page, dont_filter=True)


    def detail_page(self,response):
        desc1 = []
        desc2 = []
        for des1 in response.xpath("//div[@class='desc_content']/p/text()").extract():
            desc1.append(des1.strip())
        for des2 in response.xpath("//strong[text()='About the apartment:']/following::p/text()").extract():
            desc2.append(des2.strip())
        images = []
     
        for img in  response.xpath("//div[@class='slider_appart']/@style").extract():
            images.append(img[16:-49])

        aditem = AdItem(source = self.name,
            title =  response.xpath("//h2[@class='appName']/text()").extract_first(),
            description = "".join(desc1) +"\n"+"".join(desc2),
            monthly_rent = response.xpath("//p[contains(text(),'Monthly rent 6+ months:')]//following::p/text()").extract_first(),
        #   monthly_rent_extra_costs = monthly_rent_extra_costs,
        #   monthly_rent_total = response.xpath("//div[text()='Gesamtmiete:']//following::div[@class='artesia-value']/text()").extract_first(),
            rooms = response.xpath("//p[contains(text(),'Bedrooms')]//following::p/a/text()").extract_first(),
         #  available_from = response.xpath("//div[text()='Verfügbarkeit:']//following::div[@class='artesia-value']/text()").extract_first(),
            deposit = response.xpath("//p[contains(text(),'Security deposit:')]//following::p/text()").extract_first(),
            size_m2 = response.xpath("//p[contains(text(),'Size')]//following::p/a/text()").extract_first(),
            category = "rental_apartment",
            floor = response.xpath("//p[contains(text(),'Floor')]//following::p/a/text()").extract_first(),
            address = response.xpath("//div[@class='desc_content addresss']/text()").extract_first().strip(),
        #   reference_id =response.xpath("//td[text()='Kennung']/following::td/text()").extract_first().strip(),
            detail_url = response.url, 
            images = images,    
            )

        if TransformerTool.validate(aditem):
            yield aditem   

  
