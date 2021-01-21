
from src.fetchClassCourse import fetchDepartment
from src.fetchCourse import fetchCourse
from src.fetchParameter import fetchCurrentYearSem
from src.fetchParameter import fetchDepartment
if __name__ == '__main__':
    departmentData = fetchDepartment()
    departmentData.pop('全校')

    yr, sem = fetchCurrentYearSem()
    fetchDepartment(yr, sem)
    for key in departmentData:
        fetchCourse(yr, sem, '', departmentData[key])
