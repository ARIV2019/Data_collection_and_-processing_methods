# Написать приложение, которое собирает основные новости с сайтов lenta.ru.
# Для парсинга использовать xpath. Структура данных должна содержать:
# * название источника,
# * наименование новости,
# * ссылку на новость,
# * дата публикации


from lxml import html
import requests
from pprint import pprint
import pandas as pd

pd.set_option('display.max_columns', None)

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
main_link = 'https://lenta.ru'
req = requests.get(main_link, headers=header).text
root = html.fromstring(req)
news_link = []
data = {}

names = root.xpath("//section[@class='row b-top7-for-main js-top-seven']//*//div[@class='item']/a/text() | //div[@class='first-item']/h2/a/text()")
hrefs = root.xpath("//section[@class='row b-top7-for-main js-top-seven']//*//div[@class='item']/a/@href | //div[@class='first-item']/h2/a/@href")
date_news = root.xpath("//section[@class='row b-top7-for-main js-top-seven']//*//div[@class='item']/a//@datetime | //div[@class='first-item']/h2/a//@datetime")
link = [(main_link + hrefs[i]) for i in range(len(names))]
data['names'] = names
data['link'] = link
data['data_news'] = date_news
source = ['источник - Lenta.ru ' for i in range(len(names))]
data['source_new'] = source

news_link.append(data)

pprint(news_link)