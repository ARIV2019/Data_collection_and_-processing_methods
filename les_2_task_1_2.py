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
headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
main_link_hh ='https://hh.ru/search/vacancy?only_with_salary=false&clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text='
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
    vac_list_hh = parsed_html.findAll('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})

    all_vac_name_hh = []
    for vac in vac_list_hh:
         vac_data = {}
         vac_name = vac.find('a', {'class': 'bloko-link HH-LinkModifier'}).text
         vac_data['vac_name'] = vac_name
         vac_data['vac_site'] = site_hh
         vac_link = vac.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
         vac_data['vac_link'] = vac_link
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
        #vac_link = vac.find('a', {'class': 'icMQ_ _1QIBo f-test-link-Veduschij_sistemnyj_administrator_Zabbix _2JivQ _3dPok'})['href']
        #vac_data['vac_link'] = vac_link
        all_vac_name_sj.append(vac_data)


pprint(all_vac_name_hh)
pprint(all_vac_name_sj)