
import time
import aiohttp
import asyncio
from fake_useragent import UserAgent


async def fetch(url, i=0):
    sem = asyncio.Semaphore(10)
    headers = {
        'User-Agent': UserAgent().random
    }
    try:
        async with sem, aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=60 * 60 * 24) as response:
                r = await response.read()
                return r.decode('big5-hkscs')
    except:
        print(f'[retry][{i}] {url}')
        time.sleep(5)
        if i < 3:
            return await fetch(url, i+1)
        else:
            print(f'[fetch failed] {url}')


async def main():
    print(await fetch('https://ntut-course.gnehs.workers.dev/course/tw/'))

if __name__ == '__main__':
    asyncio.run(main())
