# 1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и
# реализовать функцию, записывающую собранные вакансии в созданную БД

# 3*)Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта

from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd
pd.set_option('display.max_columns', None)
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['VACANCY']
vac_hh = db.vac_hh
vac_sj = db.vac_sj


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
                 compens = {'min': int(compens_data[0].replace('\xa0', '')), 'max': int(compens_data[1].replace('\xa0', '')), 'type': compens_type[0]}
             else:
                 compens = {'min': int(compens_data[0].replace('\xa0', '')), 'max': 'Нет данных', 'type': compens_type[0]}
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
        main_info = vac.find('div', {'class': '_3syPg _1_bQo _2FJA4'}).findChild()
        vac_link = site_sj + main_info.find('a')['href']
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
                    compens = {'min': int(compens_data[0].replace('\xa0', '')), 'max': int(compens_data[1].replace('\xa0', '')), 'type': 'руб.'}
                else:
                    compens = {'min': int(compens_data[0].replace('\xa0', '')), 'max': 'Не указано', 'type': 'руб.'}
        vac_data['compens'] = compens

        all_vac_name_sj.append(vac_data)


# 3*)Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта
# в существующих вакансиях происходит обновление значения ОПЛАТА!!

def vac_hh_bd():
    i = 0
    all_link_hh = []
    for i in range(len(all_vac_name_hh)):
        if all_vac_name_hh[i]['vac_link'] not in all_link_hh:
            vac_hh.insert_one(all_vac_name_hh[i])
            all_link_hh.append(all_vac_name_hh[i]['vac_link'])
        else:
            vac_hh.update_one({'vac_link': all_vac_name_hh[i]['vac_link']}, {'$set': {'compens': all_vac_name_hh[i]['compens']}})

def vac_sj_bd():
    i = 0
    all_link_sj = []
    for i in range(len(all_vac_name_sj)):
        if all_vac_name_sj[i]['vac_link'] not in all_link_sj:
            vac_sj.insert_one(all_vac_name_sj[i])
            all_link_sj.append(all_vac_name_sj[i]['vac_link'])
        else:
            vac_sj.update_one({'vac_link': all_vac_name_sj[i]['vac_link']}, {'$set': {'compens': all_vac_name_sj[i]['compens']}})

vac_hh_bd()
vac_sj_bd()
pprint(len(all_vac_name_hh))
pprint(len(all_vac_name_sj))



