from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import settings
import bs4



def auth():
    driver.get('https://agrobizneskarta.ru/')
    driver.find_element_by_xpath('//div[@id="loginzone"]/a').click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'USER_LOGIN')))
    driver.find_element_by_name('USER_LOGIN').send_keys(settings.LOGIN)
    driver.find_element_by_name('USER_PASSWORD').send_keys(settings.PASSW)
    driver.find_element_by_name('Login').click()




def get_celldata(data_id):    
    driver.find_element_by_xpath(f'//div[@data-id="{data_id}"]/span').click()
    director = driver.find_element_by_xpath('//div[@class="contact_info_inner"]/p').text
    contacts = driver.find_element_by_xpath('//div[@class="contact_info_inner"]/p[2]').text
    email = driver.find_element_by_xpath('//div[@class="contact_info_inner"]/p/a').text
    print(director, contacts, email)



def get_html(url):
    driver.get(url)
    return driver.page_source

def id_list(html):  # Список id, чтобы потом по ним искать "Пока"
    soup = bs4.BeautifulSoup(html, 'lxml')
    list_id = soup.find_all('div', class_='el_header_block')
    ids = []
    for item in list_id:
        id = item.get('data-id')
        ids.append(id)    
    return ids






options = webdriver.FirefoxOptions()
options.headless = False
driver = webdriver.Firefox(executable_path=os.getcwd() + '/geckodriver', options=options)

auth()
page_html = get_html(settings.rastenie)
list_id = id_list(page_html)
for id in list_id:
    get_celldata(id)

    








# TODO авторизоваться
# TODO должен быть список УРЛов, по которому буду итерироваться при помощи for
# TODO 

