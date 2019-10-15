import requests

token = input('Введите код доступа: ')
headers = {
'User-agent': 'Chrome/77.0.3865.90,(Windows NT 10.0; Win64; x64)',
'Authorization': token}

req = requests.get('https://m.vk.com/basic-auth', headers=headers)
print('Заголовки: \n',  req.headers)
