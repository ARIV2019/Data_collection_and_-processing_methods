# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы) с сайта superjob.ru и hh.ru.
# Приложение должно анализировать несколько страниц сайта(также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
#         *Наименование вакансии
#         *Предлагаемую зарплату (отдельно мин. и отдельно макс.)
#         *Ссылку на саму вакансию
#         *Сайт откуда собрана вакансия
# По своему желанию можно добавить еще работодателя и расположение.
# Данная структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas.

from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests
import re

import pandas as pd
pd.set_option('display.max_columns', None)

headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
main_link_hh = 'https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&text='
main_link_sj = 'https://www.superjob.ru/vacancy/search/?keywords='
search_words = input('Введите ключевые слова:  ')
page_count = int(input('Сколько страниц обработать: '))
page = '&page='
site_hh = 'https://hh.ru'
site_sj = 'https://www.superjob.ru'


number_page = 0
for number_page in range(page_count):
    html = requests.get(main_link_hh+search_words+page+str(number_page), headers=headers).text
    parsed_html = bs(html, 'lxml')
    vac_list_hh = parsed_html.findAll('div', {'class': 'vacancy-serp-item'})

    all_vac_name_hh = []
    for vac in vac_list_hh:
         vac_data = {}
         vac_name = vac.find('a', {'class': 'bloko-link HH-LinkModifier'}).text
         vac_data['vac_name'] = vac_name
         vac_data['vac_site'] = site_hh
         vac_link = vac.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
         vac_data['vac_link'] = vac_link
         vac_city = vac.find('span', {'class': 'vacancy-serp-item__meta-info'})
         city_data = re.findall('([А-Я]+[а-я]*)', vac_city.getText())
         city = city_data[0]
         vac_data['city'] = city
         vac_compens = vac.find('div', {'class': 'vacancy-serp-item__compensation'})
         if not vac_compens:
             compens = {'min': 'Нет данных', 'max': 'Нет данных', 'type': 'Нет данных'}
         else:
             compens_data = re.findall('(\d+[\s\d]*)', vac_compens.getText())
             compens_type = re.findall('([А-яA-z]{3}\.*)', vac_compens.getText())
             if not compens_type:
                 compens_type = 'руб.'
             if len(compens_data) > 1:
                 compens = {'min': compens_data[0], 'max': compens_data[1], 'type': compens_type[0]}
             else:
                 compens = {'min': compens_data[0], 'max': 'Нет данных', 'type': compens_type[0]}
         vac_data['compens'] = compens

         all_vac_name_hh.append(vac_data)

number_page = 1
for number_page in range(page_count):
    html = requests.get(main_link_sj + search_words + page + str(number_page), headers=headers).text
    parsed_html = bs(html, 'lxml')
    vac_list_sj = parsed_html.findAll('div', {'class': '_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr'})

    all_vac_name_sj = []
    for vac in vac_list_sj:
        vac_data = {}
        vac_name = vac.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).text
        vac_data['vac_name'] = vac_name
        vac_data['vac_site'] = site_sj
        vac_link = site_sj + vac.find('a', {'class': 'icMQ_ _1QIBo f-test-link-Programmist_Python_(udaljonno) _2JivQ _3dPok'})['href']
        vac_data['vac_link'] = vac_link
        vac_city = vac.find('span', {'class': '_3mfro f-test-text-company-item-location _9fXTd _2JVkc _3e53o'})
        city_data = re.findall('([А-Я]+[а-я]*)', vac_city.getText())
        city = city_data[0]
        vac_data['city'] = city
        vac_compens = vac.find('span', {'class': '_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'})
        if not vac_compens or vac_compens.getText() == 'По договорённости':
            compens = {'min': 'Нет данных', 'max': 'Нет данных', 'type': 'Нет данных'}
        else:
            compens_data = re.findall('[от\s]*(\d+\s\d+)', vac_compens.getText())
            if not compens_data:
                compens = {'min': 'Нет данных', 'max': 'Нет данных', 'type': 'Нет данных'}
            else:
                if len(compens_data) > 1:
                    compens = {'min': compens_data[0], 'max': compens_data[1], 'type': 'руб.'}
                else:
                    compens = {'min': compens_data[0], 'max': 'Не указано', 'type': 'руб.'}
        vac_data['compens'] = compens

        all_vac_name_sj.append(vac_data)


print(f'Вакансий с сайта {site_hh} по запросу <{search_words}> - {len(all_vac_name_hh)} штук.')
#pprint(all_vac_name_hh)
print(f'Вакансий с сайта {site_sj} по запросу <{search_words}> - {len(all_vac_name_sj)} штук.')
#pprint(all_vac_name_sj)

data_sj = pd.DataFrame(all_vac_name_sj)
data_hh = pd.DataFrame(all_vac_name_hh)

pprint(data_sj.head(5))
pprint(data_hh.head(5))