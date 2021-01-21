import asyncio
from src.fetchClassCourse import fetchDepartmentData
from src.fetchCourse import fetchCourse
import sys
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('no argument')
        sys.exit()
    yr = sys.argv[1]
    for sem in range(1, 2+1):
        print(f'[fetch] Year:{yr} Sem:{sem}')
        asyncio.run(fetchDepartmentData(yr, sem))
        asyncio.run(fetchCourse(yr, sem))
