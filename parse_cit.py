import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.97 Safari/537.36 Vivaldi/1.94.1008.44"
}
    
doc = requests.get("https://finewords.ru/po-temam", headers).text
soup = BeautifulSoup(doc, 'lxml')
url_list = soup.find('ul', {'class': "wp-tag-cloud"}).find_all('a')

file_cits = open('cits.txt', 'w')

counter = 0

print(len(url_list))

for url in url_list:
    new_url = url.get('href')
    print(new_url)
    
    page = requests.get(new_url, headers).text
    new_soup = BeautifulSoup(page, 'lxml')
    cits = new_soup.find_all('div', {'class' : 'cit'})
    for text in cits:
        counter += 1
        print(counter)
        try:
            if len(text.p.text) < 200:
                file_cits.write(text.p.text + '\t\n')
        except:
            pass
    #break
    
file_cits.close()    