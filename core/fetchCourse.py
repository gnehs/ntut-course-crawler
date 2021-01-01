from bs4 import BeautifulSoup
import os
import json
import re
import time
import requests
from core.fetch import fetch


def fetchCourseDescription(url='Curr.jsp?format=-2&code=3204094'):
    url = 'https://aps.ntut.edu.tw/course/tw/'+url
    result = fetch(url)
    soup = BeautifulSoup(result.text, 'lxml')('tr')
    soup.pop(0)
    courseCode = soup[0]('td')[0].text.replace('\n', '').strip()
    courseNameEng = soup[0]('td')[2].text.replace('\n', '').strip()
    courseDescription = soup[1]('td')[0].text
    courseDescriptionEng = soup[2]('td')[0].text
    return courseCode, courseNameEng, courseDescription, courseDescriptionEng


def fetchSyllabus(url='ShowSyllabus.jsp?snum=281841&code=11189'):
    url = 'https://aps.ntut.edu.tw/course/tw/'+url
    result = fetch(url)
    soup = BeautifulSoup(result.text, 'lxml')('tr')
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


def fetchCourse(year=109, sem=2, keyword=''):
    try:
        os.makedirs(f'./dist/{year}/{sem}/course')
    except:
        pass
    payload = {
        'stime': '0',
        'year': year,
        'matric': '7',
        'sem': sem,
        'unit': '**',
        'cname':  keyword.encode('cp950'),
        'ccode': '',
        'tname': '',
        'PN': 'ON',
    }
    for i in range(6+1):
        payload['D'+str(i)] = 'ON'
    for i in range(6+13):
        payload['P'+str(i)] = 'ON'

    print(f'[fetch] 正在取得課程列表...')
    result = requests.post(
        'https://aps.ntut.edu.tw/course/tw/QueryCourse.jsp', data=payload)
    result.encoding = 'cp950'
    # 以 Beautiful Soup 解析 HTML 程式碼
    soup = BeautifulSoup(result.text, 'lxml')("tr")
    # remove useless data
    soup.pop(0)
    soup.pop()
    soup.pop()
    soup.pop()
    table_data = []
    print(f'[fetch] 開始擷取 {len(soup)} 堂課')
    for row in soup:
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
        print(f'[fetch] {courseId}|{courseName}')
        # fetch description
        courseCode, courseNameEng, courseDescription, courseDescriptionEng = fetchCourseDescription(
            rowData[1]('a')[0].get('href'))
        # fetch syllabus

        def parseSyllabus(d):
            syllabusData = []
            for i in d:
                syllabusData.append(fetchSyllabus(i.get('href')))
            with open(f'./dist/{year}/{sem}/course/{courseId}.json', 'w') as outfile:
                json.dump(syllabusData, outfile)
        parseSyllabus(rowData[20]('a')),
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
        time.sleep(.1)  # 我是好寶寶

    with open(f'./dist/{year}/{sem}/main.json', 'w') as outfile:
        json.dump(table_data, outfile)
    print('All done!')


if __name__ == '__main__':
    fetchCourse()
