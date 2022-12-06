import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time

path_data = 'data/scraped_apartments.json'
path_links = 'data/link/links.json'

index = [
    'id',
    'name',
    'date',
    'type_tx',
    'zone',
    'price',
    'price_currency',
    'aviable',
    'expenses',
    'currency_expenses',
    'total_surface',
    'total_covered',
    'ambients',
    'bedrooms',
    'bathrooms',
    'mascots',
    'antiquity',
    'orientation'
]

try:
    scraped_apartments = pd.read_json(path_data)
except:
    scraped_apartments = pd.DataFrame([])
    pass

links_df = pd.read_json(path_links)[0]

errores = []
list_objs = []


already_used_id_list = scraped_apartments['id'].array

only_new_links = []

for x in links_df:
    id = int(x.split('-')[1])
    if not id in already_used_id_list:
        only_new_links.append(x)

print(len(only_new_links), len(links_df))


driver = webdriver.Chrome(executable_path='chromedriver')

for i, link in enumerate(only_new_links):

    id = int(link.split('-')[1])
    count_round = (len(already_used_id_list) + i)
    result = (count_round / len(links_df)) * 100
    print(round(result, 4), ' %') 

    driver.get(link)
    # Delete Cookies Windows
    try:
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[1]/div[2]/button[1]').click()
    except:
        pass

    expenses = None
    expenses_currency = None
    total_surface = 0
    total_covered = 0
    ambients = 0
    bedrooms = 0
    bathrooms = 0
    mascots = False
    antiquity = None
    available = None
    orientation = None

    try:
        driver.find_element(By.XPATH, '/html/body/main/div/div[2]/section/div[1]/div/div/div[2]/div[1]')
        continue
    except:

        table_catacteristics = driver.find_elements(
            By.CLASS_NAME, 'andes-table__row')
        name = driver.find_element(
            By.XPATH, '/html/body/main/div/div[4]/div/div[1]/div[1]/div/div[1]/div/div[2]/h1').text
        type_tx = driver.find_element(
            By.XPATH, '/html/body/main/div/div[4]/div/div[1]/div[1]/div/div[1]/div/div[1]/span').text
        #saller_name = driver.find_element(By.XPATH, '')
        try:
            date = driver.find_element(
                By.XPATH, '/html/body/main/div/div[4]/div/div[1]/div[1]/div/div[1]/div/p').text
        except:
            date = driver.find_element(
                By.XPATH, '/html/body/main/div/div[4]/div/div[1]/div[1]/div/div[1]/div/div[3]/p').text
        price = driver.find_element(
            By.XPATH, '/html/body/main/div/div[4]/div/div[1]/div[1]/div/div[2]/div/div/span/span[3]').text
        price_currency = driver.find_element(
            By.XPATH, '/html/body/main/div/div[4]/div/div[1]/div[1]/div/div[2]/div/div/span/span[2]').text
        zone_base = driver.find_elements(
            By.CLASS_NAME, 'andes-breadcrumb__link')
        for zone1 in zone_base:
            zone = zone1


        for row in table_catacteristics:

            title = row.find_element(By.TAG_NAME, 'th').text
            data = row.find_element(By.TAG_NAME, 'td').text

            if 'Ambientes' in title:
                ambients = data

            if 'Expensas' in title:
                expenses = data.split(' ')[0]
                expenses_currency = data.split(' ')[1]

            if 'Antigüedad' in title:
                antiquity = data.split(' ')[0]

            if 'Dormitorios' in title:
                bedrooms = data

            if 'Orientación' in title:
                orientation = data

            if 'Superficie total' in title:
                total_surface = data.split(' ')[0]

            if 'Superficie cubierta' in title:
                total_covered = data.split(' ')[0]

            if 'mascotas' in title:
                mascots = data

            if 'Baños' in title:
                bathrooms = data

        obj = {
            'id': id,
            'name': name,
            'date': date,
            'type_tx': type_tx,
            'zone': zone.text,
            'price': price.replace('.', ''),
            'price_currency': price_currency,
            'aviable': available,
            'expenses': expenses,
            'currency_expenses': price_currency,
            'total_surface': total_surface,
            'total_covered': total_covered,
            'ambients': ambients,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'mascots': mascots,
            'antiquity': antiquity,
            'orientation': orientation
        }

        if scraped_apartments.empty == False:
            scraped_apartments = pd.read_json(path_data)

        new_row = pd.DataFrame([obj], index=[len(scraped_apartments)])
        
        scraped_apartments = pd.concat([scraped_apartments, new_row])
        
        print(scraped_apartments)
        
        #scraped_apartments = scraped_apartments.append(
        #    obj, ignore_index=True)

        scraped_apartments.to_json(path_data)
