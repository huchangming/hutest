from selenium import webdriver
import time
import unittest
import random
from functools import wraps



from config import config_for_ui
from remind import now_time
from log import log_d


# 错误时打印错误日志及截图给报告,装饰器函数，报错截图，不报错正常执行。
def get_image(test_case):
    @wraps(test_case)       # 装饰器自身不会修改被装饰的__name__属性
    def inner(self,*args, **kwargs):
        try:
            test_case(self,*args, **kwargs)    # 正常每次都会返回被装饰的case去执行,当遇到错误case失败时,执行异常模块
        except Exception as e:
            time_str_map = now_time.get_times()
            self.ele.get_screenshot_as_file('../tours_report/images/%s.png' % time_str_map)
            print('screenshot:', time_str_map, '.png')
            self.my_log.error(" %s 用例不通过:=====%s" % (test_case.__name__, str(e)))   # 日志尽量输出详细原始日志
            raise Exception(" %s 测试不通过" % test_case.__name__)
        else:            #未抛出异常时，才会执行
            self.my_log.debug(" %s 测试通过" % test_case.__name__)
    return inner



# 测试类
class Tours(unittest.TestCase):
    my_log = log_d.logger('../tours_report/log.txt')
    my_log.info('**************************开始执行测试！************************************************************')
    name = '胡昌明TEST%s' % random.randint(1,2000000)
    url_pc = config_for_ui.url_pc['003']
    url_m = config_for_ui.url_m['003']
    def setUp(self):
        self.ele = webdriver.Chrome()


    # 游客下单
    @get_image
    def test_pc_visitor_create_order(self):
        self.ele.get(self.url_pc)
        self.ele.maximize_window()
        self.ele.implicitly_wait(5)
        try:
            self.ele.find_element_by_css_selector('[title="最小化"]').click()
        except:
            pass
        self.ele.find_elements_by_class_name('has-day.hand')[1].click()
        try:
            if self.ele.find_element_by_class_name('add-services'):

                self.ele.find_element_by_xpath('//span[text()="请选择"]').click()
                time.sleep(2)
                self.ele.find_element_by_css_selector('div.choose>span+div>div:nth-child(2)>ul:nth-child(2)>li').click()
        except:
            pass
        time.sleep(1)
        self.ele.find_element_by_xpath('//span[text()="立即预定"]').click()
        time.sleep(1)
        self.ele.find_element_by_css_selector('div.go-login.hand').click()
        time.sleep(1)
        n = 0
        while 1:
            try:
                self.ele.find_element_by_xpath('//input[@placeholder="请输入姓名"]').send_keys(self.name)
                self.ele.find_element_by_xpath('//input[@placeholder="请输入电话号码"]').send_keys('17628055996')
                self.ele.find_element_by_xpath('//input[@placeholder="请输入您的邮箱"]').send_keys('hhhmu@qq.com')
                self.ele.find_element_by_xpath('//input[@placeholder="请输入中文姓名"]').send_keys('胡昌明TEST')
                self.ele.find_element_by_xpath('//input[@placeholder="姓（拼音或英文）"]').send_keys('Hu')
                self.ele.find_element_by_xpath('//input[@placeholder="名（拼音或英文）"]').send_keys('ChangMing')
                self.ele.find_element_by_xpath('//input[@placeholder="请选择"]').click()
                time.sleep(1)
                self.ele.find_element_by_xpath('//li[text()="中国"]').click()
                self.ele.find_element_by_xpath('//input[@placeholder="请输入护照号码"]').send_keys('G232432543')
                self.ele.find_element_by_xpath('//span[text()="男"]').click()
                self.ele.find_element_by_xpath('//input[@placeholder="请填写电话号码"]').send_keys('17628055999')
                self.ele.find_element_by_tag_name('textarea').send_keys('这是一单自动创建订单,测试TEST！')
                self.ele.find_element_by_xpath('//span[text()="同意以下协议并付款"]').click()
                time.sleep(3)
            except Exception as e:
                n+=1
                if n == 3:
                    raise Exception(str(e))
                self.ele.refresh()
                continue
            break
        time.sleep(2)
        html = self.ele.page_source
        if '微信支付' not in html:
            raise Exception('创建订单失败')
        self.ele.find_element_by_xpath('//span[text()="微信支付"]').click()
        time.sleep(4)
        flag = self.ele.find_element_by_css_selector('[class="code-img"]').size['height']
        self.assertTrue(flag>200, msg='微信支付跳转失败')   # 断言 ，ture通过，不通过时进入装饰器执行截图操作


    # 登录并用户下单
    @get_image
    def test_pc_custom_create_order(self):
        self.ele.get(self.url_pc)
        self.ele.maximize_window()
        self.ele.implicitly_wait(5)
        ele = self.ele
        ele.find_element_by_css_selector('[class="set-list set-logIn"]').click()
        ele.find_element_by_xpath('//span[text()="账号密码登录"]').click()
        time.sleep(2)
        ele.find_element_by_css_selector('[placeholder="请输入手机或邮箱"]').send_keys(config_for_ui.user['username'])
        ele.find_element_by_css_selector('[placeholder="请输入密码"]').send_keys(config_for_ui.user['password'])
        time.sleep(1)
        ele.find_element_by_xpath('//span[text()="登录"]').click()
        time.sleep(5)
        # 当次断言失败，不会继续执行，跳出该case，并且程序不会走入装饰器内。
        self.assertTrue('您好，请登录' not in ele.page_source,msg='登录跳转失败')
        try:
            ele.find_element_by_css_selector('[title="最小化"]').click()
        except:
            pass
        ele.find_elements_by_class_name('has-day.hand')[1].click()
        try:
            if ele.find_element_by_class_name('add-services'):
                ele.find_element_by_xpath('//span[text()="请选择"]').click()
                time.sleep(2)
                ele.find_element_by_css_selector('div.choose>span+div>div:nth-child(2)>ul:nth-child(2)>li').click()
        except:
            pass
        time.sleep(1)
        ele.find_element_by_xpath('//span[text()="立即预定"]').click()
        time.sleep(3)
        ele.find_element_by_xpath('//input[@placeholder="请输入姓名"]').send_keys(self.name)
        ele.find_element_by_xpath('//input[@placeholder="请输入电话号码"]').send_keys('17628055996')
        ele.find_element_by_xpath('//input[@placeholder="请输入您的邮箱"]').send_keys('hhhmu@qq.com')
        ele.find_element_by_css_selector('[class="user-item hand"]').click()
        ele.find_element_by_tag_name('textarea').send_keys('这是一单用户自动创建订单,测试！')
        ele.find_element_by_xpath('//span[text()="同意以下协议并付款"]').click()
        time.sleep(5)
        html = self.ele.page_source
        if '微信支付' not in html:
            raise Exception('创建订单失败')
        self.ele.find_element_by_xpath('//span[text()="微信支付"]').click()
        time.sleep(4)
        # flag = 1 if self.ele.find_element_by_css_selector('[class="code-img"]') else 0
        flag = self.ele.find_element_by_css_selector('[class="code-img"]').size['height']
        self.assertTrue(flag>200,msg='微信支付跳转失败')    # 断言 ，ture通过，未通过时并执行进入装饰器执行截图操作
    # m站加载慢
    def test_m_visitor_create_order(self):
        self.ele.get(self.url_m)
        self.ele.set_window_size(400,1000)
        self.ele.implicitly_wait(5)
        self.ele.find_element_by_css_selector('.g-price-item').click()
        time.sleep(2)
        self.ele.find_element_by_xpath('//span[text()="下一步"]').click()
        time.sleep(1)
        self.ele.find_element_by_xpath('//span[text()="暂未选择接送机服务"]').click()
        time.sleep(1)
        self.ele.find_element_by_css_selector('[class="van-radio__label"]').click()
        time.sleep(1)
        self.ele.find_element_by_xpath('//span[text()="确认"]').click()
        time.sleep(1)
        self.ele.find_element_by_xpath('//span[text()="暂未选择行程"]').click()
        time.sleep(1)
        self.ele.find_elements_by_css_selector('[class="van-radio__label"]')[-3].click()
        time.sleep(1)
        self.ele.find_element_by_xpath('//span[text()="确认"]').click()
        #录入游客信息
        self.ele.find_element_by_css_selector('[placeholder="请输入英文姓"]').send_keys('huchangm')
        self.ele.find_element_by_css_selector('[placeholder="请输入英文名"]').send_keys('test')
        self.ele.find_element_by_css_selector('[placeholder="须与证件上一致"]').send_keys('G232111245')
        self.ele.find_element_by_css_selector('[placeholder="填写联系人姓名"]').send_keys('test')
        self.ele.find_element_by_css_selector('[placeholder="必填，用于接收信息"]').send_keys('17628055996')
        self.ele.find_element_by_css_selector('[placeholder="必填，用于接收电子客票"]').send_keys('hhhmu@qq.com')
        self.ele.find_element_by_css_selector('[placeholder="选填，你可备注预订相关要求"]').send_keys('m站自动化测试订单')
        time.sleep(1)
        self.ele.find_element_by_xpath('//span[text()="下一步"]').click()
        time.sleep(2)
        # 断言登录




    def tearDown(self):
        pass
        self.ele.close()
        self.my_log.info('*********************测试结束，关闭driver！**************************************************')


if __name__=='__main__':
    unittest.main()