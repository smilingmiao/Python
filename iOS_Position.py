import requests
from bs4 import BeautifulSoup
import re


BASE_URL = 'https://www.lagou.com/zhaopin/iOS/'



headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

data = requests.get(BASE_URL, headers=headers).content
soup = BeautifulSoup(data, 'html.parser')
pos_list = soup.select('ul.item_con_list > li')
for i in pos_list:
    # print(i.find('li')['data-company'])
    print(i.find('h3').get_text())
    print(i.find('span', attrs={'class': 'add'}).get_text())
    li_b_l = i.find('div', attrs={'class': 'li_b_l'})
    print(li_b_l.find(text=re.compile('经验')))
    print(li_b_l.find('span', attrs={'class': 'money'}).get_text())
    print('------------------------------------------------------')