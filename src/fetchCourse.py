import asyncio
from bs4 import BeautifulSoup
import os
import json
import re
import requests
import random
import time
from os import path

if __name__ == '__main__':
    from fetchUrl.fetchUrl import fetch
else:
    from .fetchUrl.fetchUrl import fetch
if __name__ == '__main__':
    from fetchParameter import fetchDepartment
else:
    from .fetchParameter import fetchDepartment

table_data = []


async def fetchCourseDescription(url='Curr.jsp?format=-2&code=1419976'):
    url = 'https://aps.ntut.edu.tw/course/tw/'+url
    result = await fetch(url)
    soup = BeautifulSoup(result, 'lxml')('tr')
    soup.pop(0)
    courseCode = soup[0]('td')[0].text.replace('\n', '').strip()
    courseNameEng = soup[0]('td')[2].text.replace('\n', '').strip()
    courseDescription = soup[1]('td')[0].text
    courseDescriptionEng = soup[2]('td')[0].text
    return courseCode, courseNameEng, courseDescription, courseDescriptionEng


async def fetchSyllabus(url='ShowSyllabus.jsp?snum=281841&code=11189'):
    url = 'https://aps.ntut.edu.tw/course/tw/'+url
    result = await fetch(url)
    soup = BeautifulSoup(result, 'lxml')('tr')
    soup.pop(0)
    soup.pop(0)
    return dict(
        name=soup[0]('th')[1].text,
        email=soup[1]('th')[1].text.replace(
            '\n', '').replace('\r', '').strip(),
        latestUpdate=soup[2]('th')[1].text,
        objective=soup[3]('textarea')[0].text,
        schedule=soup[4]('textarea')[0].text,
        scorePolicy=soup[5]('textarea')[0].text,
        materials=soup[6]('textarea')[0].text,
        foreignLanguageTextbooks=re.findall(
            r'使用外文原文書：(.)', soup[6]('td')[0].text)[0] == '是')


def post(url, payload):
    result = requests.post(
        'https://ntut-course.gnehs.workers.dev/course/tw/QueryCourse.jsp', data=payload)
    result.encoding = 'big5-hkscs'
    return result.text


async def courseWorker(row, year, sem):
    await asyncio.sleep(random.randint(1, 60*5))
    try:
        def parseLinks(d):
            res = []
            for i in d:
                res.append({
                    'name': i.text,
                    'link': i.get('href'),
                    'code':  re.findall(r'code=(.+)', i.get('href'))[0]
                })
            return res
        rowData = row("td")
        courseId = rowData[0].text.replace('\n', '')
        courseName = rowData[1].text.replace('\n', '')

        print(f'[fetch][{courseId}]{courseName}')
        # fetch description
        courseCode, courseNameEng, courseDescription, courseDescriptionEng = await fetchCourseDescription(
            rowData[1]('a')[0].get('href'))

        # fetch syllabus
        async def parseSyllabus(d):
            filepath = f'./dist/{year}/{sem}/course/{courseId}.json'
            if not path.exists(filepath):
                syllabusData = []
                for i in d:
                    syllabusData.append(await fetchSyllabus(i.get('href')))
                with open(filepath, 'w') as outfile:
                    json.dump(syllabusData, outfile, ensure_ascii=False)

        await parseSyllabus(rowData[20]('a'))
        table_data.append({
            'id': courseId,
            'code': courseCode,
            'name': {
                'zh': courseName,
                'en': courseNameEng
            },
            'description': {
                'zh': courseDescription,
                'en': courseDescriptionEng
            },
            'stage': rowData[2].text.replace('\n', ''),
            'credit': rowData[3].text.replace('\n', ''),
            'hours': rowData[4].text.replace('\n', ''),
            'courseType': rowData[5].text.replace('\n', ''),
            'class': parseLinks(rowData[6]('a')),
            'teacher': parseLinks(rowData[7]('a')),
            'time': {
                'sun': rowData[8].text.split(),
                'mon': rowData[9].text.split(),
                'tue': rowData[10].text.split(),
                'wed': rowData[11].text.split(),
                'thu': rowData[12].text.split(),
                'fri': rowData[13].text.split(),
                'sat': rowData[14].text.split(),
            },
            'classroom': parseLinks(rowData[15]('a')),
            'people': rowData[16].text.replace('\n', ''),
            'peopleWithdraw': rowData[17].text.replace('\n', ''),
            'ta': parseLinks(rowData[18]('a')),
            'language': rowData[19].text.replace('\n', ''),
            'notes': rowData[21].text.replace('\n', ''),
        })
    except:
        pass


async def fetchAllCourse(year=109, sem=2, keyword=''):
    payload = {
        'stime': '0',
        'year': year,
        'matric': "'0','1','4','5','6','7','8','9','A','C','D','E','F'",
        'sem': sem,
        'unit': '**',
        'cname': keyword.encode('cp950'),
        'ccode': '',
        'tname': '',
        'PN': 'ON',
    }
    for i in range(6+1):
        payload['D'+str(i)] = 'ON'
    for i in range(13+1):
        payload['P'+str(i)] = 'ON'

    print(f'[fetch] 請求該學期所有課程列表...')

    # 以 Beautiful Soup 解析 HTML 程式碼
    soup = BeautifulSoup(
        post('https://ntut-course.gnehs.workers.dev/course/tw/QueryCourse.jsp', payload), 'lxml')("tr")
    # remove useless data
    try:
        soup.pop(0)
        soup.pop()
        soup.pop()
        soup.pop()
    except:
        pass
    print(f'[fetch] 開始擷取 {len(soup)} 堂課')

    tasksPool = []
    for i in soup:
        tasksPool.append(courseWorker(i, year, sem))
    await asyncio.gather(*tasksPool)
    with open(f'./dist/{year}/{sem}/all.json', 'w') as outfile:
        json.dump(table_data, outfile, ensure_ascii=False)


async def fetchCourse(year=109, sem=2, keyword=''):
    try:
        os.makedirs(f'./dist/{year}/{sem}/course')
    except:
        pass
    await fetchAllCourse(year, sem, keyword)
    departmentData = await fetchDepartment()
    for key in departmentData:
        payload = {
            'stime': '0',
            'year': year,
            'matric': departmentData[key],
            'sem': sem,
            'unit': '**',
            'cname':  keyword.encode('cp950'),
            'search':  keyword.encode('cp950'),
            'ccode': '',
            'tname': '',
            'PN': 'ON',
        }
        for i in range(6+1):
            payload['D'+str(i)] = 'ON'
        for i in range(13+1):
            payload['P'+str(i)] = 'ON'

        print(f'[fetch] 請求課程列表：{key}')

        soup = BeautifulSoup(
            post('https://ntut-course.gnehs.workers.dev/course/tw/QueryCourse.jsp', payload), 'lxml')("tr")
        try:
            soup.pop(0)
            soup.pop()
            soup.pop()
            soup.pop()
        except:
            pass

        result_json_data = []
        courseIds = [s('td')[0].text.replace('\n', '') for s in soup]
        for course in table_data:
            if course['id'] in courseIds:
                result_json_data.append(course)

        filename = 'main' if key == '日間部四技' else key
        with open(f'./dist/{year}/{sem}/{filename}.json', 'w') as outfile:
            json.dump(result_json_data, outfile, ensure_ascii=False)
    print('All done!')


if __name__ == '__main__':
    asyncio.run(fetchCourse())
