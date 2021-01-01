
from fetch import fetch
from bs4 import BeautifulSoup
import re
import json


def fetchClass(url):
    url = 'https://aps.ntut.edu.tw/course/tw/'+url
    departmentData = fetch(url)

    soup = BeautifulSoup(departmentData.text, 'lxml')
    res = []
    for item in soup.findAll('a', href=re.compile(r'^Subj.jsp?')):
        res.append({
            'name': item.text,
            'href': item.get('href')
        })
    return res


def fetchAllClass(year=109, sem=2):
    print(f'[fetch] 正在取得系所列表...')
    url = f'Subj.jsp?format=-2&year={year}&sem={sem}'
    url = 'https://aps.ntut.edu.tw/course/tw/'+url
    departmentsData = fetch(url)

    soup = BeautifulSoup(departmentsData.text, 'lxml')
    res = []
    for department in soup.findAll('a', href=re.compile(r'^Subj.jsp?')):
        res.append({
            'name': department.text,
            'href': department.get('href'),
            'class': fetchClass(department.get('href'))
        })

    with open(f'./dist/{year}/{sem}/department.json', 'w') as outfile:
        json.dump(res, outfile)


if __name__ == '__main__':
    fetchAllClass()
