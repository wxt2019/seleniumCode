# coding:utf8
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from comment.Excelrw import Writer
from comment.logger import logger
import threading, os, time


class APP:
    '''
    auther: wxh
    app 关键字类
    '''

    # 初始化参数
    def __init__(self, writer):
        # 保存打开的APP
        self.driver = ''
        # 用于写入结果
        self.writer = writer
        # 用于保存/传递参数
        self.param = ''
        # 用于保存appium端口
        self.port = ''

    def runappium(self, appiumPath, port, t):

        '''
        多线程启动appium
        :param appiumPath: appium安装路径
        :param port: appium启动的端口号
        :param time:  等待时间
        :return:
        '''

        # 执行cmd命令
        def run(cmd):
            res = os.system(cmd)
            print('运行子线程')
            return res

        if port == '':
            self.port = '4723'
        self.port = port

        # 多线程执行
        cmd = 'netstat -aon | findstr ' + port + ' | findstr LISTENING'
        result = run(cmd)
        self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
        self.writer.write(self.writer.row, self.writer.clo+1, '端口被占用')
        # 执行命令的结果0是端口被占用，1是端口未被占用
        if result == 0:
            logger.error('端口被占用')
            return
        else:
            # 启动appium
            cmd = 'node ' + appiumPath + '\\resources\\app\\node_modules\\appium\\build\\lib\\main.js -p ' + port
            # cmd = 'ipconfig'
            th = threading.Thread(target=run, args=(cmd,))
            print('运行主线程')
            th.start()
            self.writer.write(self.writer.row,self.writer.clo,'PASS')
            try:
                t = int(t)
            except Exception as e:
                print(e)
                t = 5
            time.sleep(t)

    def runapps(self, confs, t):
        '''
        连接设备、打开app
        :param confs:
        :param t:
        :return:
        '''

        # 默认配置
        conf = {
            "platformName": "Android",
            "platformVersion": "6.0.1",
            "deviceName": "127.0.0.1:7555",
            "appPackage": "com.tencent.mm",
            "appActivity": ".ui.LauncherUI",
            "noReset": "true",
            "unicodeKeyboard": "true",
            "resetKeyboard": "true"
        }

        try:
            # 将数据传进来
            confs = eval(confs)
            for key in confs:
                conf[key] = confs[key]
        except Exception as e:
            logger.warn("app配置数据错误")
            logger.exception(e)

        # 多台设备连接时，需要指定设备
        conf['uid'] = conf['deviceName']
        try:
            # 保障设备已连接上
            os.system("adb connect " + conf['uid'])
        except Exception as e:
            logger.exception(e)

        try:
            # 连接设备打开app
            print('http://localhost:' + self.port.__str__() + "/wd/hub")
            self.driver = webdriver.Remote('http://localhost:' + self.port + "/wd/hub", conf)
            self.writer.write(self.writer.row, self.writer.clo, 'PASS')
        except Exception as e:
            self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            self.writer.write(self.writer.row, self.writer.clo+1, '启动app失败')
            logger.exception(e)
        # 设置隐式等待
        self.driver.implicitly_wait(t)
        # self.driver.back()
        return self.driver

    # 关闭appium
    def close(self):
        # 使用关闭node来关闭appium
        try:
            os.system('taskkill /F /IM node.exe')
            self.writer.write(self.writer.row, self.writer.clo, 'PASS')
            return True
        except Exception as e:
            self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            self.writer.write(self.writer.row, self.writer.clo + 1, '关闭appium失败')
            logger.error("关闭appium失败！")
            return False

        # 'el1 = driver.find_element_by_xpath("//android.widget.RelativeLayout[@content-desc=\"更多功能按钮\"]/android.widget.ImageView")
        # el1.click()
        # el2 = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout")
        # el2.click()
        # el3 = driver.find_element_by_id("com.tencent.mm:id/kh")
        # el3.click()
        # el4 = driver.find_element_by_id("android:id/text1")
        # el4.click()
        # el4.send_keys("18924916436")
        # el5 = driver.find_element_by_id("com.tencent.mm:id/kh")
        # el5.click()
        # el6 = driver.find_element_by_accessibility_id("头像")
        # el6.click()

    def __find_element(self, ojb):
        '''
        支持三种定位方式：id ,xpath ,accessibility_id
        :param ojb: id ,xpath ,accessibility_id
        :return: 定位的元素
        '''

        # 兼容多种定位
        try:
            if ojb.find(':id') > -1:
                ele = self.driver.find_element_by_id(ojb)

            else:
                if ojb.startswith('/'):
                    ele = self.driver.find_element_by_xpath(ojb)

                else:
                    ele = self.driver.find_element_by_accessibility_id(ojb)

        except Exception as e:
            logger.exception(e)
            return None
        return ele

    def click(self, locat):
        time.sleep(3)
        try:
            self.__find_element(locat).click()
            self.writer.write(self.writer.row, self.writer.clo, 'PASS')
        except Exception as e:
            self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            logger.exception(e)


    def clear(self, locat):
        '''
        清空指定位置控件的内容
        :param locat: 定位
        :return:
        '''
        try:
            self.__find_element(locat).click()
            self.writer.write(self.writer.row, self.writer.clo, 'PASS')
        except Exception as e:
            self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            logger.error('无法定位到该元素！')
            logger.exception(e)

    def sendkeys(self, locat, content):
        '''
        在指定元素中输入内容
        :param locat: 定位方式
        :param content: 输入内容
        :return: 无
        '''
        try:
            self.__find_element(locat).send_keys(content)
            self.writer.write(self.writer.row, self.writer.clo, 'PASS')
        except Exception as e:
            self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            logger.exception(e)

    def swipe(self, p1, p2):
        '''
        滑动屏幕从p1到p2点
        :param p1: 初坐标
        :param p2: 末坐标
        :return:
        '''
        # TouchAction(driver).press(x=362, y=423).move_to(x=356, y=713).release().perform()
        try:
            # p1=''
            p1 = p1.split(',')
            x1 = int(p1[0])
            y1 = int(p1[1])
            p2 = p2.split(',')
            x2 = int(p2[0])
            y2 = int(p2[1])
            TouchAction(self.driver).press(x1,y1).move_to(x2,y2).release().perform()
            self.writer.write(self.writer.row, self.writer.clo, 'PASS')
        except Exception as e:
            self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            logger.exception(e)

    def back(self):
        '''
        返回操作
        :return:
        '''

        time.sleep(2)
        try:
            self.driver.back()
            self.writer.write(self.writer.row, self.writer.clo, 'PASS')
        except Exception as e:
            self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            logger.exception(e)

    def sleep(self, t):
        '''
        响应时间
        :param t:时间
        :return:
        '''
        try:
            t = int(t)
        except Exception as e:
            t = 5
        time.sleep(t)
