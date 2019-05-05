# coding:utf8

from comment.Excelrw import Reader, Writer,logger
from keywords.httpkeys import HTTP
from keywords.webkeys import WEB
# from keywords.soapkeys import SOAP
from keywords.appkeys import APP
import inspect, sys
import datetime



# 获取方法
def getfunc(funkeys, line):
    fun = None
    try:
        # 通过用例excel中的第4列关键字，获取对应关键类对象（funkeys）的方法
        fun = getattr(funkeys, line[3])
    except Exception as e:
        logger.exception(e)
        print('获取函数')
    print(fun)
    return fun


# 获取方法参数
def getfuncparam(fun):
    if fun:
        args = inspect.getfullargspec(fun).__str__()
        print(args)
        args = args[args.find('args=') + 5:args.find(', varargs')]
        args = eval(args)
        args.remove('self')
        lenparam = len(args)
        return lenparam
    else:
        return 0


# 执行一条用例
def runcase(lenline, fun, line):
    # print('参数长度：' + str(lenline))
    # print(lenline)
    if fun is None:
        print("函数不存在")
        pass

    if lenline < 1:
        fun()
        return

    if lenline < 2:
        print(line[4])
        fun(line[4])
        return

    if lenline < 3:
        fun(line[4], line[5])
        return

    if lenline < 4:
        fun(line[4], line[5], line[6])
        return


def runCases(casepath, resultpath, keystype):
    reader = Reader()
    reader.open_excel(casepath)
    writer = Writer()
    writer.copy_open(casepath, resultpath)
    # 声明一个变量存放关键字类对象
    keys = ''
    # 判断执行的哪个关键字类
    if keystype.__contains__('http'):
        keys = HTTP(writer)
    if keystype.__contains__('web'):
        keys = WEB(writer)
    # if keystype.__contains__('soap'):
    #     keys = soap(writer)
    if keystype.__contains__('app'):
        keys = APP(writer)


    # 读取sheet页
    sheetnames = reader.get_sheets()
    print(sheetnames)
    # writer没有sheet,默认是在第一个sheet中
    writer.set_sheet(sheetnames[0])
    # 在结果excel中写入开始执行时间
    writer.write(1, 3, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    for sheet in sheetnames:
        # 切换sheet页
        reader.set_sheet(sheet)
        writer.set_sheet(sheet)
        # 默认结果写在第7列
        writer.clo = 7
        # 遍历每个sheet的每行
        for i in range(reader.rows):
            # 获取所有行，list类型
            caseline = reader.readline()
            # 判断如果是分组信息就跳过
            if len(caseline[0]) > 0 or len(caseline[1]) > 0:
                pass
            else:
                print(caseline)
                # 赋值所在行数
                writer.row = i

                fun = getfunc(keys, caseline)
                # print(fun)
                lenargs = getfuncparam(fun)
                # print(lenargs)
                runcase(lenargs, fun, caseline)

    writer.set_sheet(sheetnames[0])
    # 在结果excel中写入开始执行时间
    writer.write(1, 4, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    writer.save_close()



# runCases()
