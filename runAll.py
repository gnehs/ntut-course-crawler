
from core.fetchDepartment import fetchDepartment
from core.fetchCourse import fetchCourse
from core.fetchYearSem import fetchAllYearSem
if __name__ == '__main__':
    yearList = fetchAllYearSem()
    for i in yearList:
        for j in yearList[i]:
            fetchDepartment(i, j)
            fetchCourse(i, j)
