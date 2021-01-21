

if __name__ == '__main__':
    from fetchUrl.fetchUrl import fetch
else:
    from .fetchUrl.fetchUrl import fetch

from bs4 import BeautifulSoup


def fetchCurrentYearSem():
    res = fetch('https://aps.ntut.edu.tw/course/tw/QueryCurrPage.jsp')
    soup = BeautifulSoup(res.text, 'lxml')
    yr = int(soup.find("select", {"name": "year"}).find(
        "option", {"selected": ""}).text)
    sem = int(soup.find("select", {"name": "sem"}).find(
        "option", selected=True).get('value'))
    return yr, sem


def fetchDepartment():
    res = fetch('https://aps.ntut.edu.tw/course/tw/QueryCurrPage.jsp')
    soup = BeautifulSoup(res.text, 'lxml')
    yr = soup.find("select", {"name": "matric"})('option')
    res = {}
    for item in yr:
        res[item.text] = item.get('value')
    res.pop('全校')
    return res


def fetchAllYear():
    res = fetch('https://aps.ntut.edu.tw/course/tw/QueryCurrPage.jsp')
    soup = BeautifulSoup(res.text, 'lxml')
    yr = soup.find("select", {"name": "year"})('option')
    res = {'years': []}

    for item in yr:
        res['years'].append(item.text)
    print('::set-output name=matrix::', res)


if __name__ == '__main__':
    print(fetchAllYear())
