# coding:utf8
from comment import mysql_init, runCases
from comment.Excelresult import ExcelResult
from comment.mail import Mail
import sys
from comment import logger

# class Running():
# 定义接受测试用例路径
casepath = ''
# 定义接受存放测试用执行结果
resultpath = ''
# 定义运行用例的类型
keystype = ''
# 默认相对路径
path = '.'
try:
    # 接受命令运行时输入的用例地址
    casepath = sys.argv[1]
    print(casepath)
except Exception as e:
    casepath = ''

if casepath == '':
    # 如果没有输入测试用例的路径就给出默认值,可以修改默认用例直接执行以测试使用
    # casepath = path + '/lib/cases/HTTP接口用例.xls'
    casepath = path + '/lib/cases/app用例.xls'
    resultpath = path + '/lib/results/result-app用例.xls'

else:
    # 输入的为绝对路径，则测试用例使用输入的路径
    if casepath.find(':') > 0:
        resultpath = path + '/lib/results/result-' + casepath[casepath.rfind('\\') +2:]
    else:
        logger.info('测试用例路径不合法！')

# casepath = path + '/lib/cases/HTTP接口用例.xls'
# resultpath = path + '/lib/results/result-HTTP接口用例.xls'

# 初始化数据库表
initsql = mysql_init.Mysqlinit('./lib/conf/conf.txt')
print(initsql.conf)
initsql.init_mysql('D:\\MyToolsdocs\\userinfo.sql')
c = casepath[casepath.rfind('\\') + 1:]
print('获取的用例' + str(c))
# 判断运行的哪个关键字类
if c.__contains__('HTTP'):
    keystype = 'http'
if c.__contains__('app'):
    keystype = 'app'
if c.__contains__('SOAP'):
    keystype = 'soap'
if c.__contains__('web'):
    keystype = 'web'

# 运行制定的测试用例
# runCases.runCases(casepath, resultpath, keystype)
runCases.runCases(casepath, resultpath, keystype)
# 根据执行后的结果统计测试数据，输出测试报告
res = ExcelResult()
results = res.getresult_dict(resultpath)
mail = Mail()
# 调用邮件html格式
html = mail.mailhtml
# 替换报告统计的数据
html = html.replace('title', '接口测试')
if results['status'] == 'PASS':
    html = html.replace('status', "PASS")
else:
    html = html.replace('<font style="font-weight: bold;font-size: 14px;color: #00d800;">status</font>',
                        '<font style="font-weight: bold;font-size: 14px;color: red;">FAIL</font>')
html = html.replace('passrate', results['rate'] + '%')
html = html.replace('casecount', results['counts'])
html = html.replace('runtype', results['runtype'])
html = html.replace('starttime', results['starttime'])
html = html.replace('endtime', results['stoptime'])
mail.send_mail(html)
