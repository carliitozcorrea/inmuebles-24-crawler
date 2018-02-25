# -*- coding: utf-8 -*-
import scrapy
import re
import json


class SaleCdmxSpider(scrapy.Spider):
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(page_number=settings.getint("PAGE_NUMBER"))

    def __init__(self, page_number):
        print('page number: ', page_number)
        if page_number <= 1:
            self.start_urls.append('http://www.inmuebles24.com/inmuebles-en-venta-en-distrito-federal.html')
        else:
            self.start_urls.append(
                'http://www.inmuebles24.com/inmuebles-en-venta-en-distrito-federal-pagina-%s.html' % page_number)

    name = 'sale_cdmx'
    allowed_domains = ['www.inmuebles24.com']
    start_urls = []

    def parse(self, response):
        print('crawling %s wait a moment...' % self.start_urls)

        page = response.url.split("/")[3]
        response_body = response.body
        with open(page, 'wb') as f:
            f.write(response_body)

        body = response.css('body')
        container = body.css('div.container-listado-patrocinado')
        list_section = container.css('section#listadoSection')
        ul_list = list_section.css('ul#avisos-content')
        array = []

        for li_element in ul_list.css('li.aviso'):
            object = {}
            data = li_element.css('div.aviso-data')
            data_left = data[0]
            data_right = data[1]
            object['title'] = data_right.css(
                'div.aviso-data-content div.aviso-data-head div.aviso-data-text h4.aviso-data-title a::text').extract_first().strip()
            object['price'] = data_left.css('div.aviso-data-price span.aviso-data-price-value::text').extract_first()
            object['location'] = re.sub('[\n\t]', '', ' '.join(data_right.css(
                'div.aviso-data-content div.aviso-data-head div.aviso-data-text span.aviso-data-location *::text').extract()))
            object['description'] = re.sub('[\n\t]', '', data_right.css(
                'div.aviso-data-content p.aviso-data-description::text').extract_first())
            object['bathroom'] = 0
            object['surface'] = 0
            object['bedroom'] = 0
            features = data_right.css('div.aviso-data-content ul.aviso-data-features li.aviso-data-features-value')
            for feature in features:
                text = re.sub('[\n\t]', '', ' '.join(feature.css('*::text').extract()))

                if re.match('^(\d)+\s+([B-b][a])', text):
                    object['bathroom'] = int(re.sub('[^0-9]', '', text))

                if re.search('construidos', text):
                    first = re.sub('[aA]', '-', text)
                    second = re.sub('([\sconstruido])', '', first)
                    object['surface'] = second

                if re.match('^(\d)+\s+[a]\s+(\d)+\s+([R])\w+', text):
                    c = re.sub('[a]', '-', text)
                    d = re.sub('[Rec\.\s]', '', c)
                    object['bedroom'] = d

                if re.match('^(\d)+\s+[R]', text):
                    object['bedroom'] = re.sub('[^\d]+', '', text)

            array.append(object)

        with open('data2.json', 'w') as outfile:
            json.dump(array, outfile, ensure_ascii=False)