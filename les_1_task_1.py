# . Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json


main_link = 'https://api.github.com/search/repositories'
user = input('Введите имя пользователя GITHUB : ')

req = requests.get(f'{main_link}?q=user:{user}')

if req.ok:
    data = json.loads(req.text)
    with open("data_file.json", "w", encoding="utf-8") as write_file:
        json.dump(data, write_file)

    print(f"У пользователя {user} есть депозитории  {[item['name'] for item in data['items']]}")
