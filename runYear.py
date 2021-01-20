
from src.fetchClassCourse import fetchDepartment
from src.fetchCourse import fetchCourse
import sys
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('no argument')
        sys.exit()
    yr = sys.argv[1]
    print(f'[fetch] Year:{yr}')
    for i in range(1, 2+1):
        fetchDepartment(yr, i)
        fetchCourse(yr, i)
