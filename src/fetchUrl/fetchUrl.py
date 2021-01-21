
import time
import aiohttp
import asyncio
from fake_useragent import UserAgent


async def fetch(url, i=0):
    headers = {
        'User-Agent': UserAgent().random
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=60 * 60 * 24) as response:
                r = await response.read()
                return r.decode('big5-hkscs')
    except:
        print(f'[retry][{i}] {url}')
        time.sleep(5)
        if i < 3:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=60 * 60 * 24) as response:
                    r = await response.read()
                    return r.decode('big5-hkscs')
        else:
            print(f'[fetch failed] {url}')


async def main():
    print(await fetch('https://aps.ntut.edu.tw/course/tw/'))

if __name__ == '__main__':
    asyncio.run(main())
