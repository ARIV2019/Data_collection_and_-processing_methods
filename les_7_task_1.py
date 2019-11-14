# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и
# сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient

you_mail = input('Введите свою почту: ')
you_passp = input('Введите свой пароль: ')


driver = webdriver.Chrome()
driver.get('https://passport.yandex.ru/auth/add?origin=home_desktop_ru&retpath=https%3A%2F%2Fmail.yandex.ru%2F&backpath=https%3A%2F%2Fyandex.ru')
assert "Авторизация" in driver.title
elem = driver.find_element_by_id('passp-field-login')
elem.send_keys(you_mail)
elem.send_keys(Keys.ENTER)
time.sleep(1)
elem = driver.find_element_by_id('passp-field-passwd')
elem.send_keys(you_passp)
elem.send_keys(Keys.ENTER)
time.sleep(10)
assert "Входящие — Яндекс.Почта" in driver.title

# Загрузка писем НА СТРАНИЦУ через кнопку "ЕЩЕ ПИСЬМА"
pages = 1
while True:
    try:
        button = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'nb-button _nb-large-pseudo-button "
                                                  "mail-MessagesPager-button js-message-load-more')]//span[@class='_nb-button-text']"))
        )
        button.click()
        pages +=1
        print(f'Загружена информация с {pages} страницы')
    except Exception as e:
        print(e)
        break

# В Яндексе очень запутанная система. В папке ВХОДЯЩИЕ оказались не только ссылки на входящие письма, но и ссылки на
# ЦЕПОЧКИ писем ,в которых были и входящие и исходящие письма(если письма были связаны).
# Поэтому создал отдельно список ссылок на письма и список ссылок на ЦЕПОЧКИ. Потом войдя в ссылки ЦЕПОЧЕК забрал только входящие письма.
# В цепочке может быть несколько входящих.Дополнительно вводим проверку на уникальность письма.(так как в разных
# цепочках письма дублируются)

# links - ссылки на цепочки писем в папке входящие
mes_links = driver.find_elements_by_xpath('//div[@class="mail-MessageSnippet-Wrapper"]/a[@class="mail-MessageSnippet'
                                          ' js-message-snippet toggles-svgicon-on-important toggles-svgicon-on-unread '
                                          'mail-MessageSnippet_thread"]')
links = []
for mes_link in mes_links:
    links.append(mes_link.get_attribute('href'))
# print(f'Загружено {len(links)} ссылок на ЦЕПОЧКИ писем.')
# # print(links)

# links_2 ссылки на письма в пвпке входящие без цепочек
mes_links_2 = driver.find_elements_by_xpath('//div[@class="mail-MessageSnippet-Wrapper"]/a[@class="mail-MessageSnippet'
                                            ' js-message-snippet toggles-svgicon-on-important toggles-svgicon-on-unread"]')
links_2 = []
for mes_link_2 in mes_links_2:
    links_2.append(mes_link_2.get_attribute('href'))
# print(f'Загружено {len(links_2)} ссылок на входящие письма.')
# print(links_2)

# links_3 ссылки на письма в пвпке входящие в цепочках из links
links_3 = []
for i in range(len(links)):
    driver.get(links[i])
    time.sleep(5)
    mes_link_in_chain = driver.find_elements_by_xpath('//div[@class="mail-MessageSnippet-Wrapper"]'
                                                      '/a[@class="mail-MessageSnippet js-message-snippet toggles-'
                                                      'svgicon-on-important toggles-svgicon-on-unread"]')
    for link_in_chain in mes_link_in_chain:
        links_3.append(link_in_chain.get_attribute('href'))
# print(f'Загружено {len(links_3)} ссылок на входящие письма.')
# print(links_3)

# обьединяем links_2 и  links_3 , при этом проверяя на уникальность
for i in range(len(links_3)):
    if links_3[i] not in links_2:
        links_2.append(links_3[i])
print(f'Загружено {len(links_2)} ссылок на входящие письма.')
#print(links_2)
#######################################################################
client = MongoClient('localhost', 27017)
db = client['yndex_mail']
yandex_mails = db.yandex_mails

for link_2 in links_2:
    mes = {}
    driver.get(link_2)
    time.sleep(5)
    from_whom = driver.find_element_by_xpath('//div[@class="mail-Message-Sender"]/span[@title]').text
    date = driver.find_element_by_xpath('//div[@class="mail-Message-Head-Floor mail-Message-Head-Floor_top"]/div[2]').text
    subject = driver.find_element_by_xpath('//span[@class="mail-Message-Toolbar-Subject-Wrapper"]/div').text
    texts_mail = driver.find_elements_by_xpath('//div[@class="mail-Message-Body-Content"]//p')
    texts = []
    for text_mail in texts_mail:
        texts.append(text_mail.text)
    mes['from_whom'] = from_whom
    mes['date'] = date
    mes['subject'] = subject
    mes['texts'] = texts
    yandex_mails.insert_one(mes)
    print(f'Сообщение по ссылке {link_2} сохранено.')

#driver.quit()