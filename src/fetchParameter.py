import asyncio
if __name__ == '__main__':
    from fetchUrl.fetchUrl import fetch
else:
    from .fetchUrl.fetchUrl import fetch

from bs4 import BeautifulSoup


async def fetchCurrentYearSem():
    res = await fetch('https://ntut-course.gnehs.workers.dev/course/tw/QueryCurrPage.jsp')
    soup = BeautifulSoup(res, 'lxml')
    yr = int(soup.find("select", {"name": "year"}).find(
        "option", {"selected": ""}).text)
    sem = int(soup.find("select", {"name": "sem"}).find(
        "option", selected=True).get('value'))
    return yr, sem


async def fetchDepartment():
    """ 
    res = await fetch('https://ntut-course.gnehs.workers.dev/course/tw/QueryCurrPage.jsp')
    soup = BeautifulSoup(res, 'lxml')
    yr = soup.find("select", {"name": "matric"})('option')
    res = {}
    for item in yr:
        res[item.text] = item.get('value')
    res.pop('全校')
    return res 
    """
    return {'日間部四技': "'7'", '日間部研究所(碩、博)': "'8','9'", '進修部四技': "'F'"}


async def fetchAllYear():
    res = await fetch('https://ntut-course.gnehs.workers.dev/course/tw/QueryCurrPage.jsp')
    soup = BeautifulSoup(res, 'lxml')
    yr = soup.find("select", {"name": "year"})('option')
    res = {'years': []}

    for item in yr:
        res['years'].append(item.text)
    print('::set-output name=matrix::', res)


if __name__ == '__main__':
    async def main():
        await fetchAllYear()
        print(await fetchDepartment())
    asyncio.run(main())
