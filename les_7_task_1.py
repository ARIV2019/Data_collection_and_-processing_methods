# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и
# сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
you_mail = input('Введите свою почту: ')
you_passp = input('Введите свой пароль: ')

driver = webdriver.Chrome()
driver.get('https://passport.yandex.ru/auth/add?origin=home_desktop_ru&retpath=https%3A%2F%2Fmail.yandex.ru%2F&backpath=https%3A%2F%2Fyandex.ru')
assert "Авторизация" in driver.title
elem = driver.find_element_by_id('passp-field-login')
elem.send_keys(you_mail)
elem.send_keys(Keys.ENTER)
elem = driver.find_element_by_id('passp-field-passwd')
elem.send_keys(you_passp)
elem.send_keys(Keys.RETURN)
#
# link_mail = driver.find_elements_by_class_name('mail-MessageSnippet js-message-snippet toggles-svgicon-on-important toggles-svgicon-on-unread')
# for link in link_mail:
#     driver.get(link_mail.get_attribute('href'))


#driver.quit()
