import asyncio
from src.fetchClassCourse import fetchDepartmentData
from src.fetchCourse import fetchCourse
import sys


async def main():
    yr = int(sys.argv[1])
    sem = int(sys.argv[2])
    print(f'[fetch] Year:{yr} Sem:{sem}')
    await fetchDepartmentData(yr, sem)
    await fetchCourse(yr, sem)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('no argument')
        sys.exit()
    asyncio.run(main())
