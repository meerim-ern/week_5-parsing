import requests
import csv
from bs4 import BeautifulSoup

# план 
# кол-во стр 
# сформировать список урл
# собрать данные

CSV = 'kivano.csv'
HOST = "https://www.kivano.kg/"
URL = "https://www.kivano.kg/mobilnye-telefony"
HEADERS ={"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"user agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0"}

def get_html(url,params =""):
    r = requests.get(url, headers =HEADERS,params=params)
    return r
html =get_html(URL)

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_= 'product_listbox')
    cellphones =[]
    
    for item in items:
        cellphones.append(
            {
                'title': item.find('div', class_='listbox_title').get_text(strip=True),
                'link_img': HOST + item.find('div', class_='listbox_img').find('img').get('src'),
                'price': item.find('div', class_='listbox_price').get_text(strip=True)
                
                
            }
        )
    return cellphones
    



get_content(html.text)

def saving(items, path):
    with open (path, 'w', newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Nazvanie","izobrojenie","sena"])
        for item in items:
            writer.writerow([item['title'],item['link_img'],item['price']])



def parser():
    PAGENATION = int(input("Kolichestvo stranis dlya obrabotki: "))
    html = get_html(URL)
    if html.status_code ==200:
        cellphones =[]
        for page in range(1,PAGENATION):
            print(f'parsim stranisu: {page}')
            html =get_html(URL, params ={'page':page})
            cellphones.extend(get_content(html.text))
            saving(cellphones, CSV)
        print(cellphones)  
    else:
        print("Error")

parser()


    






  