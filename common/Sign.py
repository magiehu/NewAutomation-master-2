"""
开发者：赵吉宁
脚本功能：接口登录
时间：2019-10-23
"""
# encoding: utf-8
import hashlib
from urllib.parse import quote
# import requests
# from ..config.config import conf
from ..config.config import Conf
import logging


class Sign:
    def __init__(self, param):

        # 1.拿到secret的值，用来生成sign签名
        self.url, self.app_key, self.secret = Conf().api_conf()

        # 2.对入参进行处理
        self.param = self.param_fix(param)

        logging.debug(self.param)

    # 处理入参的函数
    def param_fix(self, param):

        # 1.拿到data的值
        if 'param' in param.keys():

            value = ''
            # 取param中的code值用来生成sign
            for i in param['param'].keys():
                if i[-4:].lower() == "code":
                    value = param['param'][i]
                else:
                    pass

            # 5.调用签名算法生成签名sign，并把sign赋给param，入参param处理完成
            param['sign'] = self.sign_old(value)

            return param

        else:

            data = param['data']

            # 2.对data值中的password进行md5加密
            if 'password' in data:
                password = self.md5(data['password'], letter='upper')

            # 3.加密后的password传回data中
                data['password'] = password

            # 4.对data值进行字符串处理、字符化处理并进行url编码

            param['data'] = self.url_encoding(data)

            # 5.调用签名算法生成签名sign，并把sign赋给param，入参param处理完成
            param['sign'] = self.sign(param)

            return param

    # md5加密算法，且加密后的字符串全部大写——>针对于密码、sign值（拼接之后）的加密
    @staticmethod
    def md5(data, letter):

        # 1.创建md5对象
        m = hashlib.md5()

        # 2.生成加密串，hashlib.md5(data)函数中，data参数的类型应该是byte，hash前必须把数据转换成bytes类型
        m.update(data.encode("utf-8"))

        # 3.返回经过md5加密的字符串，全部大写
        if letter == 'upper':
            md = m.hexdigest().upper()
        else:
            md = m.hexdigest().lower()
        return md

    # 签名算法：根据一定拼接方式，生成sign值——>针对于传参中sign字符串的拼接
    def sign(self, param):
        # 1.将param中的key拿出并生成列表
        param_keys = list(param.keys())

        # 2.将param_keys列表升序排序
        param_keys.sort()

        # 3.定义一个空字符串等待拼接
        string_sign = str()

        # 4.将升序排序的param_keys列表递归
        for param_key in param_keys:

            # 按照key+value的样式拼接字符串
            string_sign += param_key+str(param[param_key])


        # 5.将secret拼接到首位两端
        string_sign = self.secret + string_sign + self.secret

        # 6.对结果进行md5加密，生成最后的签名
        return self.md5(string_sign, letter='upper')

    def sign_old(self, value):

        string_sign = '{"value":'+str(value)+'},test'

        return self.md5(string_sign, letter='lower')

    # url编码——>针对于传参中data的url编码
    @staticmethod
    def url_encoding(data):
        # 1.将data转换为字符串
        string_data = str(data)

        # 2.把字符串转换为bytes类型
        string_data = string_data.encode("utf-8")

        # 3.最后进行url编码
        url_data = quote(string_data)

        return url_data
