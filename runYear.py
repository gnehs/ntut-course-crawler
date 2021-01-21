
from src.fetchClassCourse import fetchDepartment
from src.fetchCourse import fetchCourse
import sys
if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('no argument')
        sys.exit()
    yr = sys.argv[1]
    sem = sys.argv[2]
    dpmName = sys.argv[3]
    dpm = sys.argv[4]
    print(f'[fetch] Year:{yr} Sem:{sem} Department: {dpmName}')
    fetchDepartment(yr, sem)
    fetchCourse(yr, sem, '', dpm)
