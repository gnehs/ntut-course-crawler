from core.fetch import fetch
from bs4 import BeautifulSoup
import os
import json


def fetchAllYear():
    res = fetch('https://aps.ntut.edu.tw/course/tw/QueryCurrPage.jsp')
    soup = BeautifulSoup(res.text, 'lxml')
    yr = soup.find("select", {"name": "year"})('option')
    res = {'years': []}
    for item in yr:
        res['years'].append(item.text)
    print('::set-output name=matrix::', res)


def fetchCurrentYearSem():
    res = fetch('https://aps.ntut.edu.tw/course/tw/QueryCurrPage.jsp')
    soup = BeautifulSoup(res.text, 'lxml')
    yr = int(soup.find("select", {"name": "year"}).find(
        "option", {"selected": ""}).text)
    sem = int(soup.find("select", {"name": "sem"}).find(
        "option", selected=True).get('value'))
    return yr, sem


if __name__ == '__main__':
    print(fetchAllYear())
