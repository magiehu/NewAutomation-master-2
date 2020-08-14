from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import pytest
from selenium.webdriver.common.action_chains import ActionChains


class TestSetPlm:

    @pytest.mark.smoke
    # 登陆并验证页面中存在运营中心菜单
    def test_0(self, chrome_config):
        driver = chrome_config['driver']
        driver.maximize_window()
        # driver.get("https://service-wbszdh.newbanker.cn/")
        driver.get("https://service-wbs321.newtamp.cn/")
        # 等待元素出现
        self.wait_element(driver, classname='el-input__inner')
        # 定位用户名输入框并输入手机号
        elem = driver.find_element_by_xpath(
            "/html/body/section/div[1]/div/div[2]/div/div/div[2]/form/div[1]/div/div/div/input")
        elem.clear()
        elem.send_keys("18888888888")
        # 定位密码输入框并输入密码
        elem = driver.find_element_by_xpath(
            "/html/body/section/div[1]/div/div[2]/div/div/div[2]/form/div[2]/div/div/div[1]/input")
        elem.clear()
        elem.send_keys("a111111")
        # 定位登陆按钮并点击
        driver.find_element_by_xpath("/html/body/section/div[1]/div/div[2]/div/div/div[3]/button").click()
        # 等待元素出现
        self.wait_element(driver, classname='el-menu-item')
        # assert "运营中心" in self.driver.page_source, "msg=页面不存在运营中心文案"

    @pytest.mark.smoke
    # 跳转到运营中心页面
    def test_1(self, chrome_config):
        driver = chrome_config['driver']
        self.wait_element(driver, classname='el-menu-item')
        # 定位元素位置并使用js点击，点击"运营中心"按钮跳转到运营中心页面
        button = driver.find_element_by_xpath("//span[text()='运营中心']")
        driver.execute_script("arguments[0].click()", button)
        try:
            driver.switch_to.window(driver.window_handles[-1])
        except Exception as e:
            print(e)
        self.wait_element(driver, classname='el-menu-item')
        # self.assertIn("服务运营管理", driver.page_source, "msg=跳转到运营中心页面超时！")

    @pytest.mark.smoke
    # 跳转到运营方案管理页面
    def test_2(self, chrome_config):
        driver = chrome_config['driver']
        self.wait_element(driver, classname='el-menu-item')
        button = driver.find_element_by_xpath("//li[contains(text(),'运营方案管理')]")
        driver.execute_script("arguments[0].click()", button)

        # self.assertIn("收益管理方案", driver.page_source, "msg=跳转到运营方案管理页面失败！")

    @pytest.mark.smoke
    # 新增收益管理方案
    def test_3(self, chrome_config):
        driver = chrome_config['driver']
        self.wait_element(driver, 'el-menu-item')
        # 点击新增方案入口
        driver.execute_script("arguments[0].click()", driver.find_element_by_xpath("//span[contains(text(),'新增方案')]"))
        # 点击新增收益管理方案
        driver.execute_script("arguments[0].click()", driver.find_element_by_xpath("//li[contains(text(),'收益管理方案')]"))
        self.wait_element(driver, 'el-input__inner')

        # 输入方案名称
        driver.find_element_by_xpath("//input[@placeholder='输入方案名称']").send_keys(chrome_config['repayment_name'])
        # 选择回款方式
        driver.find_element_by_xpath("//input[@placeholder='请选择回款方式']").click()
        driver.execute_script("arguments[0].click()",
                              driver.find_element_by_xpath("//span[contains(text(),'一次性还本付息')]"))
        # 选择起息方式
        driver.find_element_by_xpath("//input[@placeholder='请选择起息方式']").click()
        driver.execute_script("arguments[0].click()",
                              driver.find_element_by_xpath("//span[contains(text(),'指定日起息')]"))

        # 选择期限类型
        driver.find_element_by_xpath("//input[@placeholder='请选择期限类型']").click()
        driver.execute_script("arguments[0].click()",
                              driver.find_element_by_xpath("//span[contains(text(),'指定到期日')]"))
        # 点击保存
        driver.execute_script("arguments[0].click()", driver.find_element_by_xpath("//section[contains(text(),'保存')]"))

        self.wait_element(driver, 'el-table__row')
        driver.find_element_by_xpath('//*[@id="tab-1"]').click()
        self.wait_element(driver, 'el-table__row')
        # self.assertTrue(
        #     driver.find_element_by_xpath("//a[contains(text(),{})]".format(chrome_config['repayment_name'])))

    @pytest.mark.smoke
    # 新增计算参数方案
    def test_4(self, chrome_config):
        driver = chrome_config['driver']
        self.wait_element(driver, 'el-menu-item')
        # 点击新增方案入口
        driver.execute_script("arguments[0].click()", driver.find_element_by_xpath("//span[contains(text(),'新增方案')]"))
        # 点击新增计算参数方案
        driver.execute_script("arguments[0].click()", driver.find_element_by_xpath("//li[contains(text(),'计算参数方案')]"))
        self.wait_element(driver, 'el-input__inner')
        # 输入方案名称
        driver.find_element_by_xpath("//input[@placeholder='输入方案名称']").send_keys(chrome_config['calculate_rule_name'])
        # 选择计算计息天数
        driver.find_element_by_xpath('//*[@id="pane-1"]/section/form/div[2]/div/div/div[2]/div/div[1]/input').click()
        driver.execute_script("arguments[0].click()",
                              driver.find_element_by_xpath("//span[contains(text(),'ACT/365')]"))
        # 选择小数舍入模式
        driver.find_element_by_xpath('//*[@id="pane-1"]/section/form/div[3]/div/div/div[2]/div/div[1]/input').click()
        driver.execute_script("arguments[0].click()",
                              driver.find_element_by_xpath("//span[contains(text(),'向下取整')]"))
        # 点击保存
        driver.execute_script("arguments[0].click()", driver.find_element_by_xpath("//section[contains(text(),'保存')]"))

        self.wait_element(driver, 'el-table__row')
        driver.find_element_by_xpath('//*[@id="tab-4"]').click()
        self.wait_element(driver, 'el-table__row')
        # self.assertTrue(
        #     driver.find_element_by_xpath("//a[contains(text(),{})]".format(chrome_config['calculate_rule_name'])))

    @pytest.mark.smoke
    # 新增额度管理方案
    def test_4_0(self, chrome_config):
        driver = chrome_config['driver']
        self.wait_element(driver, 'el-menu-item')
        # 点击新增方案入口
        driver.execute_script("arguments[0].click()",
                              driver.find_element_by_xpath("//span[contains(text(),'新增方案')]"))
        # 点击新增额度管理方案
        driver.execute_script("arguments[0].click()",
                              driver.find_element_by_xpath("//li[contains(text(),'额度管理方案')]"))
        self.wait_element(driver, 'el-input__inner')

        # 输入方案名称
        driver.find_element_by_xpath("//input[@placeholder='输入方案名称']").send_keys(chrome_config['limit_name'])

        # 点击保存
        driver.execute_script("arguments[0].click()",
                              driver.find_element_by_xpath("//section[contains(text(),'保存')]"))

        self.wait_element(driver, 'el-table__row')
        driver.find_element_by_xpath('//*[@id="tab-1"]').click()
        self.wait_element(driver, 'el-table__row')

    @pytest.mark.smoke
    # 新增贴息管理方案
    def test_4_1(self, chrome_config):
        driver = chrome_config['driver']
        self.wait_element(driver, 'el-menu-item')
        # 点击新增方案入口
        driver.execute_script("arguments[0].click()", driver.find_element_by_xpath("//span[contains(text(),'新增方案')]"))
        # 点击新增贴息管理方案
        self.wait_element(driver, xpath_str="//li[contains(text(),'贴息管理方案')]")
        driver.execute_script("arguments[0].click()", driver.find_element_by_xpath("//li[contains(text(),'贴息管理方案')]"))
        # 输入方案名称
        self.wait_element(driver, xpath_str="//input[@placeholder='输入方案名称']")

        driver.find_element_by_xpath("//input[@placeholder='输入方案名称']").send_keys(
            chrome_config['interest_allowance_name'])

        # 选择贴息起息方式
        self.wait_element(driver, xpath_str="//input[@placeholder='请选择']")
        driver.find_elements_by_xpath("//input[@placeholder='请选择']")[0].click()

        self.wait_element(driver, xpath_str="//span[contains(text(),'指定起息日')]")

        driver.find_element_by_xpath("//li/span[contains(text(),'指定起息日')]").click()

        # 输入贴息到期日
        self.wait_element(driver, xpath_str="//input[@placeholder='请选择']")
        driver.find_elements_by_xpath("//input[@placeholder='请选择']")[1].click()
        self.wait_element(driver, xpath_str="//span[contains(text(),'指定到期日')]")
        driver.find_element_by_xpath("//li/span[contains(text(),'指定到期日')]").click()

        # 清除readonly属性
        self.wait_element(driver, xpath_str="//input[@placeholder='请选择']")

        # 输入贴息发放时间
        driver.find_elements_by_xpath("//input[@placeholder='请选择']")[2].click()
        self.wait_element(driver, xpath_str="//span[contains(text(),'指定日发放')]")
        driver.find_element_by_xpath("//li/span[contains(text(),'指定日发放')]").click()

        self.wait_element(driver, xpath_str="//section[contains(text(),'保存')]")
        # 点击保存
        driver.find_element_by_xpath("//section[contains(text(),'保存')]").click()
        time.sleep(10)

    @pytest.mark.smoke
    # 跳转到服务运营管理页面
    def test_5(self, chrome_config):
        driver = chrome_config['driver']
        self.wait_element(driver, classname='el-menu-item')
        button = driver.find_element_by_xpath("//li[contains(text(),'服务运营管理')]")
        driver.execute_script("arguments[0].click()", button)

        # self.assertIn("产品名称", driver.page_source, "msg=跳转到服务运营管理失败！")

    @pytest.mark.smoke
    # 同步产品信息
    def test_6(self, chrome_config):
        driver = chrome_config['driver']
        # 点击同步产品信息按钮
        driver.execute_script("arguments[0].click()",
                              driver.find_element_by_xpath("//section[contains(text(),'同步产品信息')]"))
        self.wait_element(driver, 'el-table__row')
        # 此处寻找同步过来的新产品，新租户可以省略这步
        # self.wait_element(driver, xpath_str="//a[contains(text(),\'{}\')]".format(chrome_config['product_name']))
        # driver.execute_script("document.documentElement.scrollTop=10000")
        # self.assertTrue(
        #     driver.find_element_by_xpath('//*[@id="pane-1"]/section/section[1]/div[2]/div[3]/table/tbody/tr'))

    @pytest.mark.smoke
    def test_7(self, chrome_config):
        driver = chrome_config['driver']
        # 点击进入产品方案详情
        self.wait_element(driver, xpath_str="//a[contains(text(),\'{}\')]".format(chrome_config['product_name']))
        driver.find_element_by_xpath("//a[contains(text(),\'{}\')]".format(chrome_config['product_name'])).click()

        # self.assertIn('产品还没有配置相关运营方案', driver.page_source, msg="并非初始化页面！")
        self.wait_element(driver, xpath_str="//section[contains(text(),'配置运营方案')]")
        driver.execute_script("arguments[0].click()",
                              driver.find_element_by_xpath("//section[contains(text(),'配置运营方案')]"))

    @pytest.mark.smoke
    def test_8(self, chrome_config):
        driver = chrome_config['driver']
        # 点击收益管理方案输入框
        # self.assertIn('如果选择了“收益管理方案”或“贴息管理方案”，则必须选择“计算参数方案”', driver.page_source, msg="并非初始化页面！")
        self.wait_element(driver, xpath_str="/html/body/div[1]/div/div[2]/form/div[1]/div/div/div[2]/div/div[1]/input")
        driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/form/div[1]/div/div/div[2]/div/div[1]/input').click()
        # 选择收益管理方案
        driver.switch_to.default_content()
        self.wait_element(driver, xpath_str="//span[contains(text(),\'{}\')]".format(chrome_config['repayment_name']))
        driver.execute_script("arguments[0].click()",
                              driver.find_element_by_xpath(
                                  "//span[contains(text(),\'{}\')]".format(chrome_config['repayment_name'])))

        # 选择贴息管理方案
        driver.switch_to.default_content()
        self.wait_element(driver, xpath_str="//input[@placeholder='请选择']")
        driver.find_elements_by_xpath("//input[@placeholder='请选择']")[3].click()
        driver.switch_to.default_content()
        self.wait_element(driver,
                          xpath_str="//span[contains(text(),\'{}\')]".format(chrome_config['interest_allowance_name']))
        driver.execute_script("arguments[0].click()",
                              driver.find_element_by_xpath(
                                  "//span[contains(text(),\'{}\')]".format(chrome_config['interest_allowance_name'])))

        driver.find_element_by_xpath("/html/body/div[1]/div/div[2]").click()

        # 选择额度管理方案
        self.wait_element(driver, xpath_str="//input[@placeholder='请选择']")
        driver.find_elements_by_xpath("//input[@placeholder='请选择']")[2].click()
        # 选择额度管理方案
        driver.switch_to.default_content()
        self.wait_element(driver, xpath_str="//span[contains(text(),\'{}\')]".format(chrome_config['limit_name']))
        driver.execute_script("arguments[0].click()",
                              driver.find_element_by_xpath(
                                  "//span[contains(text(),\'{}\')]".format(chrome_config['limit_name'])))
        time.sleep(5)

        # 点击计算参数方案输入框
        self.wait_element(driver, xpath_str='/html/body/div[1]/div/div[2]/form/div[4]/div/div/div[2]/div/div[1]/input')
        driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/form/div[4]/div/div/div[2]/div/div[1]/input').click()
        # 选择计算参数方案
        driver.switch_to.default_content()
        self.wait_element(driver, xpath_str="/html/body/div[4]/div[1]/div[1]/ul/li[1]/span")
        driver.execute_script("arguments[0].click()",
                              driver.find_element_by_xpath(
                                  "//span[contains(text(),\'{}\')]".format(chrome_config['calculate_rule_name'])))
        # 点击确定
        self.wait_element(driver, xpath_str="//section[contains(text(),'确定')]")
        driver.find_element_by_xpath("//section[contains(text(),'确定')]").click()
        self.wait_element(driver,
                          xpath_str='//*[@id="nb-scroll-content"]/section/section/div/div[1]/div[1]/div[3]/section[3]/div[1]')

    @pytest.mark.smoke
    # 编辑收益管理方案
    def test_9(self, chrome_config):
        driver = chrome_config['driver']
        # --------------------------点击编辑收益管理方案------------------------
        self.wait_element(driver, xpath_str='//*[@id="pane-1"]/section/section/section[1]/div[1]/div[2]/div/button')
        driver.find_element_by_xpath(
            '//*[@id="pane-1"]/section/section/section[1]/div[1]/div[2]/div/button').click()
        # --------------------------点击选择方案名称输入框------------------------
        self.wait_element(driver, xpath_str="//input[@placeholder='请选择方案名称']")
        # driver.find_element_by_xpath("//input[@placeholder='请选择方案名称']").click()
        # --------------------------选择请选择方案名称------------------------
        # self.wait_element(driver, xpath_str="//span[contains(text(),'UI-收益管理')]")
        # driver.find_element_by_xpath("//span[contains(text(),'UI-收益管理')]").click()
        driver.execute_script('arguments[0].removeAttribute("readonly")',
                              driver.find_element_by_xpath("//input[@placeholder='请选择方案名称']"))
        driver.find_element_by_xpath("//input[@placeholder='请选择方案名称']").send_keys(chrome_config['repayment_name'])
        # --------------------------添加业绩比较基准------------------------
        self.wait_element(driver, xpath_str="//a[text()='添加业绩比较基准']")
        driver.find_element_by_xpath("//a[text()='添加业绩比较基准']").click()
        self.wait_element(driver, xpath_str="//input[@placeholder='请输入认购区间']")
        driver.find_elements_by_xpath("//input[@placeholder='请输入认购区间']")[0].send_keys("1")
        driver.find_elements_by_xpath("//input[@placeholder='请输入认购区间']")[1].send_keys("999999999999")
        driver.find_element_by_xpath("//input[@placeholder='请输入业绩比较基准']").send_keys("2")
        # --------------------------点击确认------------------------
        self.wait_element(driver, xpath_str="//section[contains(text(),'确认')]")
        driver.find_element_by_xpath("//section[contains(text(),'确认')]").click()
        # --------------------------选择可提前赎回------------------------
        self.wait_element(driver, xpath_str='//span[contains(text(),"是")]')
        driver.find_element_by_xpath(
            '//*[@id="pane-1"]/section/section/section[1]/div[2]/section/section/form/div[3]/div/div/div/div[2]/div/label[1]/span[1]/span').click()
        # --------------------------输入指定起息日------------------------
        driver.execute_script('arguments[0].removeAttribute("readonly")',
                              driver.find_element_by_xpath("//input[@placeholder='请选择指定起息日']"))
        driver.find_element_by_xpath("//input[@placeholder='请选择指定起息日']").send_keys('2020-08-01')
        # 从这开始没有在页面中，需要下拉滚动条
        self.wait_element(driver, xpath_str="//section[contains(text(),'保存')]")
        driver.execute_script("arguments[0].scrollIntoView(false);",
                              driver.find_element_by_xpath("//section[contains(text(),'保存')]"))
        self.wait_element(driver, xpath_str="//section[contains(text(),'保存')]")
        # --------------------------输入指定到期日------------------------
        self.wait_element(driver, xpath_str="//input[@placeholder='请选择指定到期日']")
        driver.execute_script('arguments[0].removeAttribute("readonly")',
                              driver.find_element_by_xpath("//input[@placeholder='请选择指定到期日']"))
        driver.find_element_by_xpath("//input[@placeholder='请选择指定到期日']").send_keys('2020-08-31')
        # --------------------------点击保存------------------------
        self.wait_element(driver, xpath_str="//section[contains(text(),'保存')]")
        driver.find_element_by_xpath("//section[contains(text(),'保存')]").click()

    @pytest.mark.smoke
    def test_9_0(self, chrome_config):
        driver = chrome_config['driver']
        ActionChains(driver).move_to_element(
            driver.find_element_by_xpath('//*/section/section')).perform()
        self.wait_element(driver, xpath_str='//*/section/section/section[2]/div[1]/div[2]/div/button')

        driver.execute_script("arguments[0].scrollIntoView(false);",
                              driver.find_element_by_xpath(
                                  '//*/section/section/section[2]/div[1]/div[2]/div/button'))
        self.wait_element(driver, xpath_str='//*/section/section/section[2]/div[1]/div[2]/div/button')
        # 点击额度编辑
        self.wait_element(driver, xpath_str="//*/section/section/section[2]/div[1]/div[2]/div/button/span")
        driver.find_element_by_xpath("//*/section/section/section[2]/div[1]/div[2]/div/button/span").click()

        # 输入预约总金额
        self.wait_element(
            driver,
            xpath_str='//*[@id="pane-1"]/section/section/section[2]/div[2]/section/section/form/div[2]/div/div/div/div[2]/div/input')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[2]/div/div/div/div[2]/div/input").send_keys(
            '100000')

        # 输入签约总金额
        self.wait_element(driver,
                          xpath_str='//*[@id="pane-1"]/section/section/section[2]/div[2]/section/section/form/div[3]/div/div/div/div[2]/div/input')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[3]/div/div/div/div[2]/div/input").send_keys(
            '100000')

        # 输入单笔预约额度范围
        self.wait_element(driver,
                          xpath_str='//*/section/section/section[2]/div[2]/section/section/form/div[4]/div/div[3]/div/div/div/div[2]/div[1]/input')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[4]/div/div[1]/div/div/div/div[2]/div[1]/input").send_keys(
            '1')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[4]/div/div[3]/div/div/div/div[2]/div[1]/input").send_keys(
            '10000')

        # 输入单笔签约额度范围
        self.wait_element(driver,
                          xpath_str='//*/section/section/section[2]/div[2]/section/section/form/div[5]/div/div[3]/div/div/div/div[2]/div[1]/input')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[5]/div/div[1]/div/div/div/div[2]/div[1]/input").send_keys(
            '1')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[5]/div/div[3]/div/div/div/div[2]/div[1]/input").send_keys(
            '10000')

        # 输入小额范围
        self.wait_element(driver,
                          xpath_str='//*[@id="pane-1"]/section/section/section[2]/div[2]/section/section/form/div[6]/div/div[3]/div/div/div/div[2]/div[1]/input')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[6]/div/div[3]/div/div/div/div[2]/div[1]/input").send_keys(
            '5000')

        # 输入大额范围
        self.wait_element(driver,
                          xpath_str='//*[@id="pane-1"]/section/section/section[2]/div[2]/section/section/form/div[7]/div/div[1]/div/div/div/div[2]/div[1]/input')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[7]/div/div[1]/div/div/div/div[2]/div[1]/input").send_keys(
            '5001')

        # 输入大额单笔预约额度范围
        self.wait_element(driver,
                          xpath_str='//*[@id="pane-1"]/section/section/section[2]/div[2]/section/section/form/div[8]/div/div[3]/div/div/div/div[2]/div[1]/input')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[8]/div/div[1]/div/div/div/div[2]/div[1]/input").send_keys(
            '5001')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[8]/div/div[3]/div/div/div/div[2]/div[1]/input").send_keys(
            '10000')

        # 输入大额单笔签约额度范围
        self.wait_element(driver,
                          xpath_str='//*[@id="pane-1"]/section/section/section[2]/div[2]/section/section/form/div[9]/div/div[3]/div/div/div/div[2]/div[1]/input')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[9]/div/div[1]/div/div/div/div[2]/div[1]/input").send_keys(
            '5001')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[9]/div/div[3]/div/div/div/div[2]/div[1]/input").send_keys(
            '10000')

        # 输入小额单笔预约额度范围
        self.wait_element(driver,
                          xpath_str='//*[@id="pane-1"]/section/section/section[2]/div[2]/section/section/form/div[10]/div/div[3]/div/div/div/div[2]/div[1]/input')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[10]/div/div[1]/div/div/div/div[2]/div[1]/input").send_keys(
            '1')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[10]/div/div[3]/div/div/div/div[2]/div[1]/input").send_keys(
            '5000')

        # 输入小额单笔签约额度范围
        self.wait_element(driver,
                          xpath_str='//*[@id="pane-1"]/section/section/section[2]/div[2]/section/section/form/div[11]/div/div[3]/div/div/div/div[2]/div[1]/input')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[11]/div/div[1]/div/div/div/div[2]/div[1]/input").send_keys(
            '1')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[11]/div/div[3]/div/div/div/div[2]/div[1]/input").send_keys(
            '5000')

        # 输入大额预约总人数
        self.wait_element(driver,
                          xpath_str='//*[@id="pane-1"]/section/section/section[2]/div[2]/section/section/form/div[12]/div/div/div/div[2]/div/input')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[12]/div/div/div/div[2]/div/input").send_keys(
            '10')

        # 输入大额签约总人数
        self.wait_element(driver,
                          xpath_str='//*[@id="pane-1"]/section/section/section[2]/div[2]/section/section/form/div[13]/div/div/div/div[2]/div/input')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[13]/div/div/div/div[2]/div/input").send_keys(
            '10')

        # 输入小额预约总人数
        self.wait_element(driver,
                          xpath_str='//*[@id="pane-1"]/section/section/section[2]/div[2]/section/section/form/div[14]/div/div/div/div[2]/div/input')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[14]/div/div/div/div[2]/div/input").send_keys(
            '10')

        # 输入小额签约总人数
        self.wait_element(driver,
                          xpath_str='//*[@id="pane-1"]/section/section/section[2]/div[2]/section/section/form/div[15]/div/div/div/div[2]/div/input')
        driver.find_element_by_xpath(
            "//*/section/section/section[2]/div[2]/section/section/form/div[15]/div/div/div/div[2]/div/input").send_keys(
            '10')

        # 点击保存
        self.wait_element(driver, xpath_str="//section[contains(text(),'保存')]")
        driver.find_element_by_xpath("//section[contains(text(),'保存')]").click()

    @pytest.mark.smoke
    # 编辑贴息管理方案
    def test_9_1(self, chrome_config):
        driver = chrome_config['driver']
        # --------------------------点击编辑贴息管理方案------------------------
        # 鼠标悬停
        ActionChains(driver).move_to_element(
            driver.find_element_by_xpath('//*[@id="pane-1"]/section/section')).perform()
        self.wait_element(driver, xpath_str='//*[@id="pane-1"]/section/section/section[3]/div[1]/div[2]/div/button')

        driver.execute_script("arguments[0].scrollIntoView(false);",
                              driver.find_element_by_xpath(
                                  '//*[@id="pane-1"]/section/section/section[3]/div[1]/div[2]/div/button'))
        self.wait_element(driver, xpath_str='//*[@id="pane-1"]/section/section/section[3]/div[1]/div[2]/div/button')

        driver.find_element_by_xpath('//*[@id="pane-1"]/section/section/section[3]/div[1]/div[2]/div/button').click()

        self.wait_element(driver, xpath_str="//section[contains(text(),'保存')]")

        driver.execute_script("arguments[0].scrollIntoView(false);",
                              driver.find_element_by_xpath("//section[contains(text(),'保存')]"))

        self.wait_element(driver, xpath_str="//section[contains(text(),'保存')]")

        self.wait_element("//input[@placeholder='输入贴息利率']")
        driver.find_element_by_xpath("//input[@placeholder='输入贴息利率']").send_keys("2")

        # --------------------------输入贴息起息日------------------------
        self.wait_element(driver, xpath_str="//input[@placeholder='请选择贴息指定起息日']")
        driver.execute_script('arguments[0].removeAttribute("readonly")',
                              driver.find_element_by_xpath("//input[@placeholder='请选择贴息指定起息日']"))

        driver.find_element_by_xpath("//input[@placeholder='请选择贴息指定起息日']").send_keys('2020-08-01')

        # --------------------------输入贴息到期日------------------------
        self.wait_element(driver, xpath_str="//input[@placeholder='请选择贴息指定到期日']")

        driver.execute_script('arguments[0].removeAttribute("readonly")',
                              driver.find_element_by_xpath("//input[@placeholder='请选择贴息指定到期日']"))
        driver.find_element_by_xpath("//input[@placeholder='请选择贴息指定到期日']").send_keys('2020-08-31')
        # --------------------------输入贴息指定发放时间------------------------
        self.wait_element(driver, xpath_str="//input[@placeholder='请选择贴息指定发放时间']")
        driver.execute_script('arguments[0].removeAttribute("readonly")',
                              driver.find_element_by_xpath("//input[@placeholder='请选择贴息指定发放时间']"))
        driver.find_element_by_xpath("//input[@placeholder='请选择贴息指定发放时间']").send_keys('2020-08-31')

        # --------------------------点击保存------------------------
        self.wait_element(driver, xpath_str="//section[contains(text(),'保存')]")
        driver.find_element_by_xpath("//section[contains(text(),'保存')]").click()

    @staticmethod
    def wait_element(driver, classname=None, xpath_str=None):
        try:
            wait = WebDriverWait(driver, 10)
            if classname is not None:
                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, classname)),
                           message="超时！/等待class元素:{}失败！".format(classname))
            elif xpath_str is not None:
                # wait.until(EC.visibility_of_any_elements_located((By.XPATH, xpath_str)),
                wait.until(EC.element_to_be_clickable((By.XPATH, xpath_str)),
                           message="超时！/等待xpath路径:{}失败！".format(xpath_str))
        except Exception as e:
            print(e)
        finally:
            pass


if __name__ == "__main__":
    pytest.main(['-v', '-s', '-m=smoke'])
    # pytest.main(['-v', '-s', '-m=smoke0'])
