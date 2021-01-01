from fetchDepartment import fetchDepartment
from fetchCourse import fetchCourse


def main():
    print('正在擷取資料...')
    fetchDepartment()
    fetchCourse()


if __name__ == '__main__':
    main()
