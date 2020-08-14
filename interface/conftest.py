import pytest
from faker import Faker
# from DB_fixture.mysql_db import DB_fixture
from common.tools import DisposeData
from selenium import webdriver


@pytest.fixture(scope='session')
def get_code():
    information = {
        'name': 'passport.login.security',
        'data': {
            "account": "18888888888",
            "password": "a111111",
            "returnUrl": "",
            "captcha": ""
        },
        'api': "/passport/api",
        'method': 'post'
    }
    result = DisposeData(information).response_()
    return result.get('value').split('=')[1]


@pytest.fixture(scope='session')
def get_token(get_code):
    information = {
        'name': 'passport.userinfo.bycode',
        'data': {
            "code": get_code
        },
        'api': "/passport/api",
        'method': 'post'
    }
    result = DisposeData(information).response_()
    return result.get('value').get('token')


@pytest.fixture(scope='session')
def random_massage(request):
    f = Faker(locale="zh_CN")
    massage = {
        'name': f.name() + "(JN)",
        'mobile': f.phone_number(),
        # 'mobile': request.param,
        'ID_card': f.ssn(),
        'sentence': f.sentence(),
        'number(1-3)': f.random_int(min=1, max=3),
        'number(1-2)': f.random_int(min=1, max=2),
        'number(300-400)': f.random_int(min=300, max=400),
        'number(1-400)': f.random_int(min=1, max=400),
        # 'number': request.param,
        'job': f.job()
    }

    return massage


@pytest.fixture(scope='session')
def test_add_department(random_massage, get_token):
    information = {
        'name': "old_add_department",
        'param': {
            'name': str(random_massage['job']).replace("/", ""),
            'departmentTypeCode': random_massage['number(1-2)']
        },
        'api': "/http/saas/department/addTopDept.json",
        'method': 'post'
    }
    result = DisposeData(information, get_token).response_()
    return result.get('data')


@pytest.fixture(scope='class')
def test_add_position(get_token, random_massage):
    information = {
        'name': 'old_add_position',
        'param': {
            'name': random_massage['job'],
            'propertyCode': random_massage['number(1-3)']
        },
        'api': "/http/saas/position/add.json",
        'method': 'post'
    }
    response = DisposeData(information, get_token).response_()
    return response.get('data')


@pytest.fixture(scope='session')
def chrome_config(test_add_new_product, random_massage):
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('--incognito')
    chrome_option.add_argument('--blink-settings=imagesEnabled=false')
    chrome_option.add_experimental_option('useAutomationExtension', False)
    chrome_option.add_experimental_option("excludeSwitches", ['enable-automation'])
    details = {
        'driver': webdriver.Chrome(options=chrome_option),
        'repayment_name': "UI-收益管理方案" + str(random_massage['number(1-400)']),
        'calculate_rule_name': "UI-计算参数方案" + str(random_massage['number(1-400)']),
        'interest_allowance_name': "UI-贴息管理方案" + str(random_massage['number(1-400)']),
        'limit_name': "UI-额度管理方案" + str(random_massage['number(1-400)']),
        'product_name': test_add_new_product['productName'],
    }
    return details


@pytest.fixture(scope='session')
def test_add_new_product(get_token, random_massage):
    information = {
        'name': 'npdc.producthandle.add',
        'data': {
            "templateId": 57,  # 客户模版14，测试环境57
            "objProductDtoList": [{
                "objNo": "NPDC-TRUST-BASE-MESSAGE",
                "info": {
                    "name": "接口自动化" + str(random_massage['number(1-400)']),
                    "minBuyMoney": "",
                    "productDeadline": "",
                    "Issuer": "",
                    "issuePlace": "",
                    "incomeDistributionMode": "",
                    "issueTime": "",
                    "publishScale": "",
                    "establishmentDate": "",
                    "establish": "",
                    "durationType": "",
                    "expectEarningRate": "",
                    "expectRateDescription": "",
                    "profitType": "",
                    "investmentType": "",
                    "fundCustodianBank": "",
                    "InvestmentField": "",
                    "investmentProjectLocation": "",
                    "productFeatures": "",
                    "financier": "",
                    "repaymentSource": "",
                    "resourceUse": "",
                    "riskControl": "",
                    "assetManager": "",
                    "IssuerStr": "爱建信托"
                },
                "productNo": ""
            }, {
                "objNo": "NPDC-SALE-CONFIG",
                "productNo": "",
                "info": {
                    "visibleScope": {
                        "faDept": [],
                        "faPosition": [],
                        "faTag": [],
                        "customerTag": [],
                        "faScope": -1,
                        "ifaScope": -1,
                        "customerScope": -1
                    },
                    "status": 1,
                    "statusForReservation": [1],
                    "advisorShareConfig": 1,
                    "modifyAfterStatus": '',
                    "modifyTime": "",
                    "modifyStatus": [],
                    "riskLevel": 1,
                    "statusStr": "预热中",
                    "advisorShareConfigStr": "可分享",
                    "statusForReservationStr": "预热中",
                    "riskLevelStr": "R1"
                }
            }],
            "categoryId": 1848  # 客户环境25，测试环境 1848
        },
        'api': '/npdc-web/api',
        'method': 'post'
    }
    # DisposeData(information, get_token).response_()
    details = {
        'productName': information['data']['objProductDtoList'][0]['info']['name'],
        'productNo': DisposeData(information, get_token).response_()['value']['productNo']
    }
    return details
