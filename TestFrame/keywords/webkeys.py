# coding:utf8

from selenium import webdriver
import traceback, os, time
from comment import logger
from selenium.webdriver.common.action_chains import ActionChains
from comment import logger
from comment.Excelrw import Writer

class WEB:

    def __init__(self, writer):
        self.driver = None
        # 定义相对变量
        self.path ='..'
        self.chromepath=self.path + '/lib/driver/chromedriver'
        self.geckopath = self.path +'/lib/driver/geckodriver'
        self.iepath=self.path +'/lib/driver/IEDriverServer'
        # 写入结果的excel对象
        self.writer = writer

    # 获取driver
    def getwebdriver(self, brower='cc', waittime=10):
        '''
        :param brower: 浏览器类型
        :param waittime: 等待响应时间
        :return: 返回driver浏览器
        '''
        if brower == 'cc':
            # 调用chrome浏览器
            # 去掉浏览器顶部提示条
            option = webdriver.ChromeOptions()
            option.add_argument('disable-infobars')
            # 为提高浏览的速度，获取用户的用户目录
            try:
                # 获取到userdir路径
                userdir = os.environ['USERPROFILE']
            except Exception as e:
                # 打印错误信息提示
                traceback.print_exc()
                # 没有获取到userdir路径，使用默认值
                userdir = 'C:\\Users\\MECHREVO'
            # 追加固定的地址,获取用户目录的全路径
            userdir += '\\AppData\\Local\\Google\\Chrome\\User Data'
            userdir = 'user-data-dir' + userdir
            # 添加用户目录（运行时不能运行Chrome浏览器）
            option.add_argument(userdir)
            # 创建对象driver浏览器对象
            self.driver = webdriver.Chrome(executable_path=self.chromepath, options=option)
            # 去掉 data;的出现
            # option
            # self.driver.find_element_by_name()
            return self.driver

        if brower == 'ff':
            self.driver = webdriver.Firefox(executable_path=self.geckopath)
            self.driver.implicitly_wait(waittime)
            return self.driver

        if brower == 'ie':
            self.driver = webdriver.Ie(executable_path= self.iepath)
            # self.driver.find_element_by_xpath().send_keys()
            self.driver.implicitly_wait(waittime)
            return self.driver

    # 浏览器打开url
    def openurl(self, url):
        '''
        :param url: 浏览器打开的地址
        :return:
        '''
        try:
            self.driver.get(url)
            # self.writer.write(self.writer.row,self.writer.clo, 'PASS')
            # self.writer.write(self.writer.row, self.writer.clo+1, url)
        except Exception as e:
            # self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            # self.writer.write(self.writer.row, self.writer.clo + 1, 'url错误！')
            logger.exception(e)

    # 定位元素
    def __findElement(self,location):
        location=''
        # 使用三种定位方式尝试定位
        if location.startswith('//'):
            ele = self.driver.find_element_by_xpath(location)
        else:
            # 尝试使用id定位
            try:
                ele = self.driver.find_element_by_id(location)
            except:
                try:
                    ele = self.driver.find_element_by_name(location)
                except:
                    return None
        return ele

    # 点击事件
    def click(self, location):
        try:
            self.__findElement(location).click()
            # self.writer.write(self.writer.row, self.writer.clo, 'PASS')
        except Exception as e:
            # self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            # self.writer.write(self.writer.row, self.writer.clo + 1, e)
            logger.exception(e)

    # 输入框输入数据
    def inputtext(self, location, text):
        '''
        :param location:定位
        :param text: 输入数据
        :return: 无
        '''
        try:
            self.__findElement(location).send_keys(text)
            # self.writer.write(self.writer.row, self.writer.clo, 'PASS')
        except Exception as e:
            # self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            # self.writer.write(self.writer.row, self.writer.clo + 1, e)
            logger.exception(e)

    # 鼠标悬浮操作
    def hover(self, location):
        '''
        鼠标悬浮/还可以滚动鼠标之后在找到对应的元素
        :param location: 鼠标 悬浮的控件的location
        :return:
        '''
        try:
            ele = self.__findElement(location)
            # self.writer.write(self.writer.row, self.writer.clo, 'PASS')
        except Exception as e:
            # self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            # self.writer.write(self.writer.row, self.writer.clo + 1, e)
            logger.exception(e)
        actions = ActionChains(self.driver)
        # 鼠标移动到对应元素上
        actions.move_to_element(ele).perform()

    # 切换窗口
    def to_windows(self, id):
        '''
        :param id: 窗口的下标
        :return:
        '''
        # 获取浏览器窗口
        handles = self.driver.window_handles
        # 关闭当前窗口,关闭
        self.driver.close()
        try:
            # 切换对应浏览器窗口
            self.driver.switch_to.window(handles[id])
            # self.writer.write(self.writer.row, self.writer.clo, 'PASS')
        except Exception as e:
            # self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            # self.writer.write(self.writer.row, self.writer.clo + 1, e)
            logger.exception(e)

    # 切入iframe窗口
    def in_iframe(self, location):
        try:
            self.driver.switch_to_frame(location)
        except Exception as e:
            logger.exception(e)

    # 切除iframe窗口
    def out_iframe(self):
        try:
            self.driver.switch_to.default_content()
            # self.writer.write(self.writer.row, self.writer.clo, 'PASS')
        except Exception as e:
            # self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            logger.exception(e)

    # 滑动鼠标
    def scoll(self, x, y):
        # 使用js方式滚动
        js= "window.scrollBy("+str(x)+","+str(y)+")"
        try:
            self.driver.execute_script(js)
        except Exception as e:
            logger.exception(e)

    # 验证
    def asserequals(self, location, asserttext):
        # 获取指定位置的数据
        webtext = self.__findElement(location).text

        if str(asserttext) == str(webtext):
            print('Pass')
        else:
            print('Fail')


