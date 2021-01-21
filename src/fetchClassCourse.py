
if __name__ == '__main__':
    from fetchUrl.fetchUrl import fetch
else:
    from .fetchUrl.fetchUrl import fetch
from bs4 import BeautifulSoup
import re
import json
import os
import asyncio


async def fetchClass(url):
    url = 'https://aps.ntut.edu.tw/course/tw/'+url
    departmentData = await fetch(url)
    soup = BeautifulSoup(departmentData, 'lxml')
    r = []
    for item in soup.findAll('a', href=re.compile(r'^Subj.jsp?')):
        r.append({
            'name': item.text,
            'href': item.get('href')
        })
    return r


async def appendData(department):
    res.append({
        'name': department.text,
        'href': department.get('href'),
        'class': await fetchClass(department.get('href'))
    })
    print(f'got {department.text}')

res = []


async def fetchDepartmentData(year=109, sem=2):
    try:
        os.makedirs(f'./dist/{year}/{sem}/course')
    except:
        pass
    print(f'[fetch] 正在取得系所列表...')
    url = f'Subj.jsp?format=-2&year={year}&sem={sem}'
    url = 'https://aps.ntut.edu.tw/course/tw/'+url
    departmentsData = await fetch(url)

    soup = BeautifulSoup(departmentsData, 'lxml')

    tasksList = [appendData(i) for i in soup.findAll(
        'a', href=re.compile(r'^Subj.jsp?'))]
    await asyncio.gather(*tasksList)

    with open(f'./dist/{year}/{sem}/department.json', 'w') as outfile:
        json.dump(res, outfile)


if __name__ == '__main__':
    asyncio.run(fetchDepartmentData())
