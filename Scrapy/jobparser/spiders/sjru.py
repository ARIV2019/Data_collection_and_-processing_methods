# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.f-test-link-dalshe::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancy = response.css(
            'div.f-test-vacancy-item a[class*=f-test-link][href^="/vakansii"]::attr(href)').extract()
        for link in vacancy:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css('h1 ::text').extract_first()
        salary = response.css(
               'div._3MVeX span[class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"] ::attr(content)').extract_first()
        vacancy_link = response.url
        site_scraping = self.allowed_domains[0]
        yield JobparserItem(name=name, salary=salary, vacancy_link=vacancy_link, site_scraping=site_scraping)