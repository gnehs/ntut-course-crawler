import asyncio
from src.fetchClassCourse import fetchDepartmentData
from src.fetchCourse import fetchCourse
from src.fetchParameter import fetchCurrentYearSem


async def main():
    yr, sem = await fetchCurrentYearSem()
    print(f'[fetch] Year:{yr} Sem:{sem}')
    await fetchDepartmentData(yr, sem)
    await fetchCourse(yr, sem)
if __name__ == '__main__':
    asyncio.run(main())
