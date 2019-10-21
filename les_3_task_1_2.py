# 2) Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы
# Задаем поиск зп в рублях, а выводит  в рублях  в долларах и казахской тэнге, в рамках заданных условий

from pprint import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['VACANCY']
vac_hh = db.vac_hh
vac_sj = db.vac_sj

size_salary = int(input('Больше (равно) какой зп вывести вакансии(руб): '))
rate_usd = 64
size_salary_usd = size_salary/rate_usd
rate_kzt = 6
size_salary_KZT = size_salary*rate_kzt

def salary_1(size_salary):
    objects_1 = vac_hh.find({'compens.min': {'$gte': size_salary}, 'compens.type': 'руб.'}, {'vac_name', 'compens', 'vac_link'})
    for obj_1 in objects_1:
        pprint(f"<{obj_1['vac_name']}> <{obj_1['vac_link']}> зарплата {obj_1['compens']['min']} {obj_1['compens']['type']}")

def salary_2(size_salary):
    objects_2 = vac_sj.find({'compens.min': {'$gte': size_salary}, 'compens.type': 'руб.'}, {'vac_name', 'compens', 'vac_link'})
    for obj_2 in objects_2:
        pprint(f"<{obj_2['vac_name']}> <{obj_2['vac_link']}> зарплата {obj_2['compens']['min']} {obj_2['compens']['type']}")

def salary_3(size_salary_usd):
    objects_3 = vac_hh.find({'compens.min': {'$gte': size_salary_usd}, 'compens.type': 'USD'}, {'vac_name', 'compens', 'vac_link'})
    for obj_3 in objects_3:
        pprint(f"<{obj_3['vac_name']}> <{obj_3['vac_link']}> зарплата {obj_3['compens']['min']} {obj_3['compens']['type']}, что составляет {obj_3['compens']['min']*rate_usd} руб.")

def salary_4(size_salary_usd):
    objects_4 = vac_sj.find({'compens.min': {'$gte': size_salary_usd}, 'compens.type': 'USD'}, {'vac_name', 'compens', 'vac_link'})
    for obj_4 in objects_4:
        pprint(f"<{obj_4['vac_name']}> <{obj_4['vac_link']}> зарплата {obj_4['compens']['min']} {obj_4['compens']['type']}, что составляет {obj_4['compens']['min']*rate_usd} руб.")

def salary_5(size_salary_KZT):
    objects_5 = vac_hh.find({'compens.min': {'$gte': size_salary_KZT}, 'compens.type': 'KZT'}, {'vac_name', 'compens', 'vac_link'})
    for obj_5 in objects_5:
        pprint(f"<{obj_5['vac_name']}> <{obj_5['vac_link']}> зарплата {obj_5['compens']['min']} {obj_5['compens']['type']} что составляет {int(obj_5['compens']['min']/rate_kzt)} руб.")

def salary_6(size_salary_KZT):
    objects_6 = vac_sj.find({'compens.min': {'$gte': size_salary_KZT}, 'compens.type': 'KZT'}, {'vac_name', 'compens', 'vac_link'})
    for obj_6 in objects_6:
        pprint(f"<{obj_6['vac_name']}> <{obj_6['vac_link']}> зарплата {obj_6['compens']['min']} {obj_6['compens']['type']} что составляет {int(obj_6['compens']['min']/rate_kzt)} руб.")

salary_1(size_salary)
salary_2(size_salary)
salary_3(size_salary_usd)
salary_4(size_salary_usd)
salary_5(size_salary_KZT)
salary_6(size_salary_KZT)