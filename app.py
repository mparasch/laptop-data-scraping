from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

df_final = pd.DataFrame()

def create_df(soup):
    prod_container = soup.find_all('ul', role=('tabpanel'))

    product_list = prod_container[0].find_all('li', class_='product_wrapper')

    prod = []
    for product in product_list:
        row = []

        sku = product.find_all('p', class_='sku')
        if sku:
            sku = sku[0].text[5:]
            row.append(sku)
        else:
            row.append('')

        descript = product.find_all('h2')
        if descript:
            descript = descript[0].text
            descript = descript[1:-1].split(';')
            row.append(descript[0].split(' - ')[0])
        else:
            row.append('')

        if len(descript[0].split(' - ')) > 1:
            color = descript[0].split(' - ')[1].strip()
            row.append(color)
        else:
            row.append('N/A')

        processor = extract_processor(descript)
        row.append(processor)

        clockspd = extract_clockspeed(processor)
        row.append(clockspd)

        ram = extract_RAM(descript)
        row.append(ram)

        rampower = extract_GB(ram)
        row.append(rampower)

        drive = extract_drive(descript)
        row.append(drive)

        drive_size = extract_GB(drive)
        row.append(drive_size)

        graphics = extract_graphics(descript)
        row.append(graphics)

        price = product.find_all('span', itemprop='price')
        if price:
            price = price[0].text
            row.append(price)
        else:
            row.append('')

        savings = product.find_all('span', class_='savings')
        if savings:
            savings = savings[0].text[5::]
            row.append(savings)
        else:
            row.append(' ')
        
        prod.append(row)

    df = pd.DataFrame(prod, columns=['sku', 'title', 'color','processor', 'clock speed', 'RAM','RAM_power', 'drive', 'drive_size', 'graphics', 'price', 'savings'])

    global df_final

    if df_final.empty:
        df_final = df
    else:
        df_final = df_final.append(df)

def extract_processor(descript):
    keys = ['processor', 'Processor', 'i\d']
    for i in descript:
        m = re.search('|'.join(keys), i)
        if m:
            return i
    return 'N/A'

def extract_clockspeed(processor):
    for i in processor.split(' '):
        m = re.search('GHz', i)
        if m:
            return i
    return 'N/A'

def extract_RAM(descript):
    keys = ['RAM', 'ram', 'Ram']
    for i in descript:
        m = re.search('|'.join(keys), i)
        if m:
            return i
    return 'N/A'

def extract_drive(descript):
    keys = ['SSD', 'ssd', 'Solid State', 'solid state', 'Hard Drive', 'HDD', 'Drive', 'drive']
    for i in descript:
        m = re.search('|'.join(keys), i)
        if m:
            return i
    return 'N/A'

def extract_GB(input):
    for i in input.split(' '):
        m = re.search('\dGB|\dTB|\dMB', i)
        if m:
            return i
    return 'N/A'

def extract_graphics(descript):
    keys = ['GDDR', 'Graphics']
    for i in descript:
        m = re.search('|'.join(keys), i)
        if m:
            return i
    return 'N/A'

page = 1
base = 'https://www.microcenter.com'

URL = f'{base}/search/search_results.aspx?N=4294967288&NTK=all&sortby=match&rpp=96&page={str(page)}'

all_pages = [URL]

html = requests.get(URL).text

soup = BeautifulSoup(html, 'html.parser')

status = soup.find_all('p', class_='status')
last = (int(status[0].text.split( ' ')[-2])//96) + 1

pages = range(1, last + 1)

for page in pages:
    print(f'page:{page}')
    URL = f'{base}/search/search_results.aspx?N=4294967288&NTK=all&sortby=match&rpp=96&page={page}'
    html = requests.get(URL).text
    soup = BeautifulSoup(html, 'html.parser')
    create_df(soup)

df_final.to_csv('df_final.csv')
