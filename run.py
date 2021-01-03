
from core.fetchDepartment import fetchDepartment
from core.fetchCourse import fetchCourse
from core.fetchYearSem import fetchCurrentYearSem
if __name__ == '__main__':
    yr, sem = fetchCurrentYearSem()
    fetchDepartment(yr, sem)
    fetchCourse(yr, sem)
