
from src.fetchClassCourse import fetchDepartment
from src.fetchCourse import fetchCourse
from src.fetchYearSem import fetchCurrentYearSem
if __name__ == '__main__':
    yr, sem = fetchCurrentYearSem()
    fetchDepartment(yr, sem)
    fetchCourse(yr, sem)
