
from src.fetchClassCourse import fetchDepartment
from src.fetchCourse import fetchCourse
import sys
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('no argument')
        sys.exit()
    yr = sys.argv[1]
    sem = sys.argv[2]
    print(f'[fetch] Year:{yr} Sem:{sem}')
    fetchDepartment(yr, sem)
    fetchCourse(yr, sem)
