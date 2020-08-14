# 接口自动化测试框架
>python + request + pytest + yaml实现接口测试自动化
### 一.背景
   接口测试实施在多系统的平台架构下，有着极为高效的成本收益比（当然，单元测试收益更高，但实施单元测试的成本投入更大，技术要求更高，所以应该选择更适合自身的才是最好的方案）。

接口测试天生为高复杂性的平台带来高效的缺陷检测和质量监督能力，平台复杂，系统越庞大，接口测试的效果越明显。

总的来说，接口测试是保证高复杂性系统质量的内在要求和低成本的经济利益驱动作用下的最佳方案，主要体现在如下三个方面：

1、节省了测试成本

   根据数据模型推算，底层的一个程序BUG可能引发上层的8个左右BUG，而且底层的BUG更容易引起全网的死机；接口测试能够提供系统复杂度上升情况下的低成本高效率的解决方案。

2、接口测试不同于单元测试

   接口测试是站在用户的角度对系统接口进行全面高效持续的检测。

3、效益更高

   将接口测试实现为自动化和持续集成，当系统复杂度和体积越大，接口测试的成本就越低，相对应的，效益产出就越高。
#### 运行环境：
+ python 3.6
#### 引用包：
+ requests
+ hashlib
+ urllib.parse
+ os
+ configparser
+ pymysql
+ json
+ pytest
+ faker
+ yaml
+ time
#### 测试用例书写：
##### 新接口（/XXX/api接口）yaml
```
# 新增员工
-
  datail: 新增员工
  name: passport.employee.add
  api: /passport/api
  method: post
  headers: None
  data:
        {
        name: 'None',
        email: '',
        gender: 0,
        mobile: 'None',
        deptIds: 'None',
        married: '',
        roleIds: [],s
        joinDate: '2019-11-27',
        managers: [ 0 ],
        education: 2,
        documentNo: 'None',
        employeeNo: '',
        positionId: 'None',
        defaultDept: '',
        documentType: 2
        }
  assert_type: equal
  check: 0
  DB_table:
      - wbs240
      - wbs_employee
```
##### 新接口（/XXX/api接口）testcase
```
    def test_add_employee(self,get_Token,random_massage,test_add_position):

        name = 'passport.employee.add'

        other_data = {
            'mobile':random_massage['mobile'],
            'name':random_massage['name'],
            'documentNo':random_massage['ID_card'],
            'positionId':test_add_position,
            'deptIds':[1]
        }

        response = GetYaml('add_employee',other_data=other_data,headers=get_Token).case_select(name)

        Assert(response['assert_type'], response['result']['code'], response['check'], response['result']['msg'])
        print('员工:',other_data['name'])
        Assert('IN',other_data['mobile'],'mobile',None,response['DB_table'])
```
##### 老接口（.json）yaml
```
# 添加职位
-
  datail: 新增职位
  name: old_add_position
  api: /http/saas/position/add.json
  method: post
  headers: None
  data:
        {
          param:
            {
            name: None,
            propertyCode: None
            }
        }
  assert_type: equal
  check: true
```
##### 老接口testcase
```
@pytest.fixture()
    def test_add_position(sel,get_Token,random_massage):

        name = 'old_add_position'
        other_data = {
            'param':{
                'name':random_massage['job'],
                'propertyCode':random_massage['number(1-3)']
            }
        }

        response = GetYaml('add_employee',other_data=other_data,headers=get_Token).case_select(name)

        Assert(response['assert_type'], response['result']['success'], response['check'], response['result']['msg'])
        print('职位：',other_data['param']['name'])
        return response['result']['data']
```
#### 签名算法
```angular2
class Sign:
    def __init__(self, param):

        # 1.拿到secret的值，用来生成sign签名
        self.url, self.app_key, self.secret = Conf().api_conf()

        # 2.对入参进行处理
        self.param = self.param_fix(param)

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
            string_sign += param_key+param[param_key]

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

```
>>>>>>> 接口自动化测试框架封装版
