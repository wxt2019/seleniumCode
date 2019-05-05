# -*- coding:UTF8 —*-
import json
from comment import logger
from suds.client import Client
from suds.xsd.doctor import ImportDoctor,Import


class SOAP:
    # 构造函数

    def __init__(self, writer):
        # 初始化client
        self.client =None
        # 用来存放json解析结果
        self.jsonre = {}
        # 保存数据,实现关联
        self.param = {}
        # 保存wsdl文档地址
        self.wsdlurl = ''
        # 写入的excel
        self.writer = writer
        # soap文档标准
        self.doctor = None
        # 结果
        self.result = None
        # header头
        self.header = {}

    # 设置url
    def adddoctor(self, targetNameSpace, XMLSchema='', location=''):
        # xsd的描述文档
        if XMLSchema == '':
            XMLSchema = 'http://www.w3.org/2001/XMLSchema'
        # xsd文档的路径
        if location == '':
            location = 'http://192.168.179.1:8080/inter/SOAP?xsd=1'

        imp = Import(XMLSchema, location=location)
        # 添加命名空间
        imp.filter.add(targetNameSpace)
        self.doctor = ImportDoctor(imp)
        return True

    # 设置描述文档地址
    def setwsdl(self, url):
        self.wsdlurl = url
        try:
            # 添加wsdl文档的全地址
            self.client = Client('http://localhost:8080/inter/SOAP?wsdl', doctor=self.doctor)
            self.writer.write(self.writer.row,self.writer.clo, 'PASS')
            self.writer.write(self.writer.row, self.writer.clo+1,  str(self.jsonre))
        except Exception as e:
            self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            self.writer.write(self.writer.row, self.writer.clo+1, str(self.jsonre))
            logger.error(e)


    # 访问url
    def callmethod(self, method, paramd=''):
        try:
            paramd = self.__params(paramd)
            # 将参数以、分隔
            if not paramd == '':
                paramd = paramd.split('、')
                print('paramd:' + str(paramd))

            # print(self.client.service.__getattr__)
            if paramd == '':
                self.result = self.client.service.__getattr__(method)()
            else:
                # 将参数替换成值, 当没有传参{}时，将不会执行
                self.result = self.client.service.__getattr__(method)(*paramd)

            self.jsonre = json.loads(self.result)
            print(self.jsonre)
            self.writer.write(self.writer.row, self.writer.clo, 'PASS')
            self.writer.write(self.writer.row, self.writer.clo + 1, str(self.jsonre))
        except Exception as e:
            self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            self.writer.write(self.writer.row, self.writer.clo + 1, str(self.jsonre))
            logger.exception(e)

    # 添加头
    def addheader(self, token, value):
        res = self.__params(value)
        self.header[token] = res
        try:
            self.client = Client(self.wsdlurl, doctor=self.doctor, headers=self.header)
            self.writer.write(self.writer.row, self.writer.clo, 'PASS')
        except Exception as e:
            self.writer.write(self.writer.row, self.writer.clo, 'FAIL')
            self.writer.write(self.writer.row, self.writer.clo + 1, str(value))
            logger.exception(e)

    # 删除头
    def removeheader(self, objkey):
        self.header.pop(objkey)
        self.client = Client(self.wsdlurl, doctor=self.doctor, headers=self.header)
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
        # value1 = ''
        try:
            value1 = self.__params(value)
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
        return obj

