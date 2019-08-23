from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
import time
import settings
import bs4
import openpyxl
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level = logging.INFO,
                    filename = 'agro.log'
                    )




def auth():
    logging.info('Старт авторизации') 
    driver.get('https://agrobizneskarta.ru/')
    driver.find_element_by_xpath('//div[@id="loginzone"]/a').click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'USER_LOGIN')))
    driver.find_element_by_name('USER_LOGIN').send_keys(settings.LOGIN)
    driver.find_element_by_name('USER_PASSWORD').send_keys(settings.PASSW)
    driver.find_element_by_name('Login').click()




def get_celldata(data_id):    
    driver.find_element_by_xpath(f'//div[@data-id="{data_id}"]/span').click()
    director = driver.find_element_by_xpath('//div[@class="contact_info_inner"]/p').text
    contacts = driver.find_element_by_xpath('//div[@class="contact_info_inner"]/p[2]').text
    email = driver.find_element_by_xpath('//div[@class="contact_info_inner"]/p/a').text
    logging.info('Получаем email: ' + email) 
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

def get_email(data_id):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//div[@data-id="{data_id}"]/span')))        
    driver.find_element_by_xpath(f'//div[@data-id="{data_id}"]/span').click()
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="contact_info_inner"]//p[@class="contacts"]')))
    emails = driver.find_elements_by_xpath('//div[@class="contact_info_inner"]/p/a')
    full_email_list = []
    for email in emails:
        if '@' in email.text:
            full_email_list.append(email.text)  
        elif '' in email.text:
            continue      
    email = ', '.join(full_email_list)       
    if email == '':
        raise NoSuchElementException('Email равно пустая строка')
    logging.info('Email равен ' + email)
    assert email != None, 'email равен None'
    assert email != '', 'email равен пустой строке'
    print(email)
    return email


def write_csv(sheet_name, email_list):     
    for email in email_list:
        with open(sheet_name + '.csv', 'a') as file:
            file.write(email + '\n')  
    logging.info('Записали имейлы в файл')      
    

def get_pages_count(html):
    soup = bs4.BeautifulSoup(html, 'lxml')
    try:
        count_pages = soup.find('div', class_='modern-page-navigation').find_all('a')[-2].get_text()    
        print('Общее число страниц: ' + count_pages)
        logging.info('Получаем число страниц: ' + count_pages) 
        return int(count_pages)
    except AttributeError:
        count_pages = 1
        return count_pages





options = webdriver.FirefoxOptions()
options.headless = False
driver = webdriver.Firefox(executable_path=os.getcwd() + '/geckodriver', options=options)
auth()

def one_category_handler(category, url):
    logging.info('Обрабатываем категорию ' + category)     
    page_html = get_html(url)    
    list_id = id_list(page_html) # Список id по которым ищем мыло

    email_list = []
    for id in list_id:
        try:
            email = get_email(id)
            if '@' in email:
                email_list.append(email)
            else: 
                continue            
        except NoSuchElementException:
            continue
    write_csv(category, email_list)


for cat in settings.URL_LIST:
    category, url = cat    
    pages_count = get_pages_count(get_html(url)) # Получаю число страниц
    for i in range(1, pages_count + 1):
        one_category_handler(category, url + str(i))

driver.quit()
