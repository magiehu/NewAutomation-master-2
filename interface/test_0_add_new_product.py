import pytest
from common.tools import DisposeData


# from multiprocessing import Process


class TestAddNewProductProcess:
    @pytest.mark.smoke
    @pytest.mark.smoke0
    def test_add_new_product(self, get_token, test_add_new_product):
        information = {
            'name': 'npdc.product.shelf',
            'data': {
                "no": test_add_new_product['productNo'],
                "releaseStatus": 1
            },
            'api': '/npdc-web/api',
            'method': 'post'
        }
        DisposeData(information, get_token).response_()
