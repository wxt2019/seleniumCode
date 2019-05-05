# -*- coding:UTF8 —*-
from comment.Excelrw import Reader
import time


class ExcelResult:

    def __init__(self):
        # 用来存储解析后的结果，用字典形式保存
        self.Summer = {}
        # 用来存放计算后的通过率
        self.rate = None
        # 用来存储全部用例的执行结果
        self.status = 'PASS'
        # 用来存储用例通过的数量
        self.countpass = 0
        # 用来存储用例的总数
        self.counts = 0

    def getresult_dict(self, path):
        '''
        :param path: 执行后的结果用例地址
        :return:返回结果
        '''
        self.starttome = time.time()
        reader = Reader()
        reader.open_excel(path)
        sheets = reader.get_sheets()
        for sheet in sheets:
            reader.set_sheet(sheet)
            # 以该sheet页行数遍历每行
            for i in range(reader.rows):
                caseline = reader.readline()
                # print(caseline)
                if len(caseline[0]) > 0 or len(caseline[1]) > 0:
                    pass
                else:
                    self.counts = self.counts + 1
                    # print(self.counts)
                    if caseline[7] == 'PASS':
                        self.countpass = self.countpass + 1
                    else:
                        self.status = 'FAIL'
        # 保存两位小数
        self.rate = (self.countpass * 10000 / self.counts) / 100

        # 将记过保存在dict中
        self.Summer['counts'] = str(self.counts)
        self.Summer['countpass'] = str(self.countpass)
        self.Summer['rate'] = str(self.rate)
        self.Summer['status'] = str(self.status)
        # 将结果表中记录的时间也存在dict中,结果在第一个sheet页中
        sheet0 = reader.set_sheet(sheets[0])
        # 先执行一遍读取第一行
        reader.readline()
        # 当前是读的第二行
        line = reader.readline()
        #  读取用例名
        self.Summer['runtype'] = str(line[2])
        self.Summer['starttime'] = str(line[3])
        self.Summer['stoptime'] = str(line[4])

        return self.Summer
