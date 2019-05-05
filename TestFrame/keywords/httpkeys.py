# -*- coding:UTF8 —*-
import requests, json
from comment import logger


class HTTP:
    # 构造函数

    def __init__(self, writer):
        # 初始化session变量
        self.session = requests.session()
        # 用来存放json解析结果
        self.jsonre = {}
        # 保存数据,实现关联
        self.param = {}
        # 默认url
        self.url = ''
        # 写入的excel
        self.writer = writer

    # 设置url
    def seturl(self, url):
        print(url)
        if url.startswith('http'):
            self.url = url
            # print('pass')
            self.writer.write(self.writer.row, self.writer.clo, 'PASS')
        else:
            self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            self.writer.write(self.writer.row, self.writer.clo + 1, '设置的url地址不合法')
            return self.url

    # 访问url
    def post(self, url, paramd=''):

        try:
            if url.startswith('http') or url.startswith('https'):
                url = self.url
            else:
                url = self.url + "/" + url
                # logger.info(url)

            if paramd is None or paramd == '':
                result = self.session.post(url)
            else:
                # 将参数替换成值, 当没有传参{}时，将不会执行
                data = self.__params(paramd)
                # 将字符串处理成字典
                datas = self.__todic(data)
                # print("date:"+str(datas))
                result = self.session.post(url, data=datas)

            self.jsonre = json.loads(result.text)
            print(self.jsonre)
            self.writer.write(self.writer.row, self.writer.clo, 'PASS')
            self.writer.write(self.writer.row, self.writer.clo + 1, str(self.jsonre))
        except Exception as e:
            self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            self.writer.write(self.writer.row, self.writer.clo + 1, str(self.jsonre))
            logger.exception(e)

    # 添加头
    def addheader(self, token, value):

        try:
            res = self.__params(value)
            self.session.headers[token] = res
            self.writer.write(self.writer.row, self.writer.clo, 'PASS')
        except Exception as e:
            self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            self.writer.write(self.writer.row, self.writer.clo + 1, str(value))
            logger.exception(e)

    # 删除头
    def removeheader(self, objkey):
        self.session.headers.pop(objkey)
        self.writer.write(self.writer.row, self.writer.clo, 'PASS')

    # 保存token
    def savejson(self, key, k):
        res = ''
        try:
            res = self.jsonre[key]
        except Exception as e:
            logger.exception(e)
        self.param[k] = res
        # print("保存的值：" + self.param[k])
        self.writer.write(self.writer.row, self.writer.clo, 'PASS')
        self.writer.write(self.writer.row, self.writer.clo + 1, str(res))

    # 验证
    def assertequals(self, key, value):
        value1 = ''
        try:
            value1 = self.__params(value)
            # print('value:' + str(value1))
        except Exception as e:
            logger.exception(e)
        if str(self.jsonre[key]) == str(value1):
            self.writer.write(self.writer.row, self.writer.clo, 'PASS')
            self.writer.write(self.writer.row, self.writer.clo + 1, str(self.jsonre[key]))
        else:
            self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            self.writer.write(self.writer.row, self.writer.clo + 1, str(self.jsonre[key]))

    # 字符串处理，将规定模式的{t} 形式，改成对应的参数值
    def __params(self, obj):

        for key in self.param:
            obj = obj.replace("{" + key + "}", self.param[key])
        print("{id}:" + obj)
        return obj

    # 处理参数字符创转化为字典
    def __todic(self, objstr):
        # 用来保存拆分的字典
        par = {}
        # 拆分参数
        params = objstr.split('&')
        for pa in params:
            ar = pa.split('=')
            # 当用例中参数出现没有=时，key就没有值，默认给个空值
            if len(ar) > 1:
                par[ar[0]] = ar[1]
            else:
                par[ar[0]] = ''
        return par
