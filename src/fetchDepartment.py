if __name__ == '__main__':
    from fetchUrl import fetch
else:
    from .fetchUrl import fetch

from bs4 import BeautifulSoup


def fetchDepartment():
    res = fetch('https://aps.ntut.edu.tw/course/tw/QueryCurrPage.jsp')
    soup = BeautifulSoup(res.text, 'lxml')
    yr = soup.find("select", {"name": "matric"})('option')
    res = {}
    for item in yr:
        res[item.text] = item.get('value')
    return res


if __name__ == '__main__':
    print(fetchDepartment())
