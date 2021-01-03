from core.fetch import fetch
from bs4 import BeautifulSoup
import os
import json


def fetchAllYearSem():
    res = fetch('https://aps.ntut.edu.tw/course/tw/QueryCurrPage.jsp')
    currentYr, currentSem = fetchCurrentYearSem()
    soup = BeautifulSoup(res.text, 'lxml')
    yr = soup.find("select", {"name": "year"})('option')
    yrRes = {}
    for item in yr:
        i = int(item.text)
        if currentSem > 1 or currentYr > i:
            yrRes[i] = [1, 2]
        else:
            yrRes[i] = [1]
    try:
        os.makedirs(f'./dist/')
    except:
        pass
    with open(f'./dist/main.json', 'w') as outfile:
        json.dump(yrRes, outfile)
    return yrRes


def fetchCurrentYearSem():
    res = fetch('https://aps.ntut.edu.tw/course/tw/QueryCurrPage.jsp')
    soup = BeautifulSoup(res.text, 'lxml')
    yr = int(soup.find("select", {"name": "year"}).find(
        "option", {"selected": ""}).text)
    sem = int(soup.find("select", {"name": "sem"}).find(
        "option", selected=True).get('value'))
    return yr, sem


if __name__ == '__main__':
    print(fetchAllYearSem())
