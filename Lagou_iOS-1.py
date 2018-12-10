"""
this is my first project to grab the iOS job info data from Lagou.com using Python
"""

__author__ = 'Yongxiang Miao'

import re
import time
import random
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

workbook = Workbook()
tab1 = workbook.active
tab1.title = 'iOS开发招聘'
dest_filename = 'iOS开发招聘数据.xlsx'

BASE_URL = 'https://www.lagou.com/zhaopin/iOS/'

RUN_TIME = 1

def randomChoices():
    proxy = ['http://163.125.149.106:9999',
             'http://111.121.193.214:3128',
             'https://122.72.18.35:80',
             'http://114.115.182.59:3128',
             'https://118.212.137.135:31288']
    agent = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
             'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
             'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)']

    return random.choice(proxy), random.choice(agent)


def get_html(url):
    p, a = randomChoices()
    headers = dict(Connection='keep-alive')
    headers['User-Agent'] = a
    proxies = dict(http=p)
    data = requests.get(url, headers=headers, proxies=proxies).content

    return data

def parser_html(data):
    soup = BeautifulSoup(data, 'html.parser')
    pos_list = soup.select('ul.item_con_list > li')

    company = []
    position = []
    experience = []
    salary = []
    address = []

    for i in pos_list:

        c = i.get('data-company')
        p = i.find('h3').get_text()
        a = i.find('span', attrs={'class': 'add'}).get_text()
        li_b_l = i.find('div', attrs={'class': 'li_b_l'})
        e = li_b_l.find(text=re.compile('经验'))
        e = re.sub('\s', '', e)
        s = li_b_l.find('span', attrs={'class': 'money'}).get_text()

        company.append(c)
        position.append(p)
        experience.append(e)
        salary.append(s)
        address.append(a)

    page = soup.find('a', attrs={'class': 'next'})
    if page:
        next_url = page['href']
        global RUN_TIME
        if RUN_TIME == 2:
            next_url += '?filterOption=2'
        elif RUN_TIME >= 3:
            next_url += '?filterOption=3'
        RUN_TIME += 1

        print('====================== : %s', next_url)

        return company, position, experience, salary, address, next_url
    return company, position, experience, salary, address, None

def main():

    global BASE_URL
    url = BASE_URL

    com = []
    pos = []
    exp = []
    sal = []
    add = []

    while url:
        data = get_html(url)
        co, po, ex, sa, ad, url = parser_html(data)

        com += co
        pos += po
        exp += ex
        sal += sa
        add += ad

        time.sleep(5)

    for c_, p_, e_, s_, a_ in zip(com, pos, exp, sal, add):
        col_A = 'A%s' % (com.index(c_) + 1)
        col_B = 'B%s' % (com.index(c_) + 1)
        col_C = 'C%s' % (com.index(c_) + 1)
        col_D = 'D%s' % (com.index(c_) + 1)
        col_E = 'E%s' % (com.index(c_) + 1)

        tab1[col_A] = c_
        tab1[col_B] = p_
        tab1[col_C] = e_
        tab1[col_D] = s_
        tab1[col_E] = a_

    workbook.save(filename=dest_filename)


if __name__ == '__main__':
    main()