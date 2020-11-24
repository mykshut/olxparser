import requests
from bs4 import BeautifulSoup
import csv
import io

main_url = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/krakow/'

def write_csv(result):
    with open('file.csv', 'w', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(['ser=,'])
        for item in result:
            writer.writerow( (item['name'],
                            item['price'],
                            item['address'],
                            item['url']
                            ))

def clean(text):
    return text.replace('\t', '').replace('\n', '').strip()

def get_page_data(page_url):
    r = requests.get(page_url)
    soup = BeautifulSoup(r.content)
    table = soup.find('table', {'id':'offers_table'})
    rows = table.find_all('tr', {'class':'wrap'})
    result = []
    for row in rows:
        name = clean(row.find('h3').text)
        url = row.find('h3').find('a').get('href')
        price = clean(row.find('p', {'class':'price'}).text)
        bottom = row.find('td', {'valign':'bottom'})
        address = clean(bottom.find('small', {'class':'breadcrumb x-normal'}).text)
        item = {'name':name,'price':price,'address':address, 'url':url,}
        result.append(item)
    return result

def main(main_url):
    r=requests.get(main_url)
    soup=BeautifulSoup(r.content)
    result = []
    for i in range(1, 25+1):
        print('parsing page # ' + str(i) + ' of ' + str(25))
        page_url = main_url + '?page=' + str(i)
        result+=get_page_data(page_url)
    write_csv(result)

if __name__ == '__main__':
    main(main_url)
