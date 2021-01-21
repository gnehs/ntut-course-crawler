import asyncio
from src.fetchClassCourse import fetchDepartmentData
from src.fetchCourse import fetchCourse
from src.fetchParameter import fetchCurrentYearSem
if __name__ == '__main__':
    yr, sem = fetchCurrentYearSem()
    print(f'[fetch] Year:{yr} Sem:{sem}')
    asyncio.run(fetchDepartmentData(yr, sem))
    asyncio.run(fetchCourse(yr, sem))
