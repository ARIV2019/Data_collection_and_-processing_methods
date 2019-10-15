#Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию через curl, Postman,
# Python.Ответ сервера записать в файл (приложить скриншот для Postman и curl)

import requests
import json

# поиск друзей которые сейчас на сайте
main_link = 'https://api.vk.com/method/friends.getOnline?v=5.52'
token = input('Введите свой токен в VK: ')
req = requests.get(f'{main_link}&access_token={token}')
if req.ok:
    data = json.loads(req.text)
    with open("data_file.json", "w", encoding="utf-8") as write_file:
        json.dump(data, write_file)



