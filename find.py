from time import sleep
import requests
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from datetime import datetime


page_var = 1
first_url = "https://inmuebles.mercadolibre.com.ar/departamentos/alquiler/capital-federal/_NoIndex_True"

links = []

driver = webdriver.Chrome(executable_path='chromedriver')


for i in range(1, 43):
    
    print( i / 43)

    page_var = page_var + 48
    url_base = f'https://inmuebles.mercadolibre.com.ar/departamentos/alquiler/capital-federal/_Desde_{page_var}_NoIndex_True'
    
    if i == 1:
        driver.get(first_url)
    else:
        driver.get(url_base)

    
    # Delete Cookies Windows
    try:
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[1]/div[2]/button[1]').click()
    except:
        pass

    #sleep(3)
    url_base = driver.current_url


    request = requests.get(url_base)

    soup = BeautifulSoup(request.content, 'html5lib')

    all_links = driver.find_elements(By.CLASS_NAME, 'ui-search-layout__item')

    for link in all_links:
        link_end = link.find_elements(By.TAG_NAME, 'a')
        links.append(link_end[0].get_attribute('href'))
        print(link_end[0].get_attribute('href'))

    #driver.find_element(By.CLASS_NAME, 'andes-pagination__arrow-title').click()
    #sleep(1)
    apartaments_df = pd.DataFrame(links)
    apartaments_df.to_json(f'data/link/links.json')


apartaments_df = pd.DataFrame(links)

now = datetime.now()
current_time = now.strftime("%H:%M:%S").replace(':', '_')
apartaments_df.to_json(f'data/link/links.json')

driver.close()
