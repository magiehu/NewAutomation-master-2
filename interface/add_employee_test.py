import pytest
from ..common.tools import DisposeData


# from multiprocessing import Process


class TestAddEmployeeProcess:

    def test_add_employee(self, get_token, random_massage):
        information = {
            'name': 'passport.employee.add',
            'data': {
                'name': random_massage['name'],
                'email': '',
                'gender': 0,
                'mobile': random_massage['mobile'],
                'deptIds': [20],
                # 'deptIds': [test_add_department],
                'married': '',
                'roleIds': [],
                'joinDate': '2019-11-27',
                'managers': [0],
                'education': 2,
                'documentNo': random_massage['ID_card'],
                'employeeNo': '',
                # 'positionId': test_add_position,
                'positionId': 1,
                'defaultDept': '',
                'documentType': 2
            },
            'api': '/passport/api',
            'method': 'post'

        }
        DisposeData(information, get_token).response_()


if __name__ == '__main__':

    pytest.main(['-v', '-s', "add_employee_test.py", '--capture=no'])
