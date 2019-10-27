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
main_link = 'https://mail.ru'
req = requests.get(main_link, headers=header).text
root = html.fromstring(req)
news_link_1 = []
data = {}

names = root.xpath("//div[contains(@class, 'news-item_main')]//h3/text() | //div[contains(@class, 'news-item_inline')]//a[last()]/text()")
link = root.xpath("//div[contains(@class, 'news-item_main')]/a/@href | //div[contains(@class, 'news-item__inner')]/a[last()]/@href")

date_news = []
for i in link:
    request = requests.get(i, headers=header)
    root = html.fromstring(request.text)
    date_new = root.xpath("//span[contains(@class, 'breadcrumbs')]/@datetime")
    date_new = date_new[0]
    date_news.append(date_new)
data['data_news'] = date_news


data['names'] = names
data['link'] = link
source = ['источник - Mail.ru ' for i in range(len(names))]
data['source_new'] = source

news_link_1.append(data)

pprint(news_link_1)