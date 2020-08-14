import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class TestPythonOrgSearch:
    @pytest.mark.smoke
    def test_99(self, chrome_config, test_add_new_product):

        driver = chrome_config['driver']
        try:
            driver.switch_to.window(driver.window_handles[0])
        except Exception as e:
            print(e)
        # 点击预约管理
        self.wait_element_visable(driver, 'el-menu-item')
        # 直接使用js注入的方法进行元素的定位,因为需要选择
        button = driver.find_element_by_xpath("/html/body/div[1]/section/div[1]/div[1]/div[1]/nav/ul/li[8]/ul/li[1]")
        driver.execute_script("arguments[0].click()", button)

        # 点击新增预约单按钮
        self.wait_element_visable(driver,
                                  xpath_str='//*[@id="nb-scroll-content"]/section/div[1]/div[1]/div/div[1]/section/div[1]/span')
        driver.execute_script("arguments[0].click()",
                              driver.find_element_by_xpath(
                                  '//*[@id="nb-scroll-content"]/section/div[1]/div[1]/div/div[1]/section/div[1]/span'))

        # 选择客户
        self.wait_element_visable(driver, xpath_str='//*[@id="pane-0"]/form/div[4]/div/div/div[2]/button/span')
        driver.find_element_by_xpath("//*/form/div[4]/div/div/div[2]/button/span").click()

        # driver.switch_to.default_content()
        # 点击客户
        self.wait_element_clicked(driver,
                                  xpath_str='/html/body/div[2]/div/div[2]/div/section[1]/div[2]/div[5]/div[2]/table/tbody/tr[2]/td[1]/div/label/span')
        driver.find_element_by_xpath(
            "/html/body/div[2]/div/div[2]/div/section[1]/div[2]/div[5]/div[2]/table/tbody/tr[2]/td[1]/div/label/span").click()
        # 点击确定
        self.wait_element_clicked(driver, xpath_str="//section[contains(text(),'确认')]")
        driver.find_element_by_xpath("//section[contains(text(),'确认')]").click()

        # 选择服务
        # 点击请选择
        self.wait_element_clicked(driver, xpath_str="//*/form/div[1]/div/div/div[2]/div/div[1]/input")
        driver.find_element_by_xpath("//*/form/div[1]/div/div/div[2]/div/div[1]/input").click()

        # 输入服务名称
        self.wait_element_clicked(driver, xpath_str="/html/body/div[4]/div[1]/div[1]/ul/li[1]")
        # time.sleep(3)
        driver.find_element_by_xpath("//*/form/div[1]/div/div/div[2]/div/div[1]/input").send_keys(
            test_add_new_product['productName'])

        # --------------------------------------------------------------------------------------------------------------

        # 点击服务
        # self.wait_element_clicked(driver,xpath_str="//span[contains(text(),{})]".format(test_add_new_product['productName']))
        self.wait_element_clicked(driver, xpath_str="/html/body/div[4]/div[1]/div[1]/ul/li[1]")

        # 如果这样写会定位错，定位成新投资mq3,不知道为什么
        driver.find_element_by_xpath(
            "//span[contains(text(),\'{}\')]".format(test_add_new_product['productName'])).click()

        # 点击预约额度
        self.wait_element_clicked(driver, xpath_str='//*[@id="pane-0"]/form/div[2]/div/div/div[2]/div/input')
        driver.find_element_by_xpath('//*[@id="pane-0"]/form/div[2]/div/div/div[2]/div/input').send_keys(1000)

        # 点击选择日期
        self.wait_element_clicked(driver, xpath_str="//input[@placeholder='选择日期时间']")
        # 去掉只读的属性，可以输入日期
        driver.execute_script('arguments[0].removeAttribute("readonly")',
                              driver.find_element_by_xpath("//input[@placeholder='选择日期时间']"))
        # 日期的页面不会自己收回去
        driver.find_element_by_xpath("//input[@placeholder='选择日期时间']").send_keys('2020-08-31')

        # 点击预约单状态"请选择"
        self.wait_element_clicked(driver, xpath_str="//*/form/div[6]/div/div/div[2]/div/div[1]/input")
        driver.find_element_by_xpath("//*/form/div[6]/div/div/div[2]/div/div[1]/input").click()

        # 点击已签约
        self.wait_element_clicked(driver, xpath_str="//span[contains(text(),'已签约')]")
        driver.find_element_by_xpath("//span[contains(text(),'已签约')]").click()

        # 点击实际签约金额
        self.wait_element_clicked(driver, xpath_str="//*/form/div[7]/div/div/div[2]/div/input")
        driver.find_element_by_xpath("//*/form/div[7]/div/div/div[2]/div/input").send_keys(1000)

        # 签约日期
        # 点击选择日期
        self.wait_element_clicked(driver, xpath_str="//*/form/div[8]/div/div/div[2]/div/input[@placeholder='选择日期时间']")
        # 去掉只读的属性，可以输入日期
        driver.execute_script('arguments[0].removeAttribute("readonly")', driver.find_element_by_xpath(
            "//*/form/div[8]/div/div/div[2]/div/input[@placeholder='选择日期时间']"))
        # 日期的页面不会自己收回去
        driver.find_element_by_xpath("//*/form/div[8]/div/div/div[2]/div/input[@placeholder='选择日期时间']").send_keys(
            '2020-08-31')

        # 点击确定
        self.wait_element_clicked(driver, xpath_str="//section[contains(text(),'确定')]")
        driver.find_element_by_xpath("//section[contains(text(),'确定')]").click()
        # time.sleep(5)

    @staticmethod
    def wait_element_visable(driver, classname=None, xpath_str=None):
        try:
            wait = WebDriverWait(driver, 10)
            if classname is not None:
                wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, classname)))
            elif xpath_str is not None:
                wait.until(EC.visibility_of_any_elements_located((By.XPATH, xpath_str)))
        except Exception as e:
            print(e)
        finally:
            pass

    @staticmethod
    def wait_element_clicked(driver, classname=None, xpath_str=None):
        try:
            wait = WebDriverWait(driver, 10)
            if classname is not None:
                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, classname)))
            elif xpath_str is not None:
                wait.until(EC.element_to_be_clickable((By.XPATH, xpath_str)))
        except Exception as e:
            print(e)
        finally:
            pass
