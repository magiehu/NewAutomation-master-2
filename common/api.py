# encoding: utf-8
"""
开发者：赵吉宁
脚本功能：接口登录
时间：2019-10-23
"""
import requests
from ..common.Sign import Sign
# from common.Sign import Sign
import json
import logging


class ApiCall(Sign):

    # 将token值传入请求头，实现接口的调用
    def api_call(self, token, api, method='get'):
        logging.debug(self.param)

        if str(api)[-4:] == 'json':

            param = "data={}".format(json.dumps(self.param))
            header = {
                "token": token,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded'
            }

        else:
            param = self.param
            header = {
                "token": token,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
            }

        if method == 'post':
            response = requests.post(self.url + api, params=param, headers=header)

        else:
            response = requests.get(self.url + api, params=param, headers=header)

        result = response.json()

        return result
