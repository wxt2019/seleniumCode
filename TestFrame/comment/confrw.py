# coding:utf8
from comment.logger import logger


# 读、写txt文件的内容，读取内容以list类型保存
class Confrw:

    # 打开文件
    def __init__(self, path, q='r', conding='utf8'):
        # 用来存储读取的每行数据
        self.data = []
        # 打开的文件
        self.f = None
        if q == 'r':
            # 逐行读取
            for line in open(path, encoding=conding):
                self.data.append(line)

            # 将末尾换行符替换
            for n in range(self.data.__len__()):
                # 处理非法字符
                self.data[n] = self.data[n].encode('utf-8').decode('utf-8-sig')
                self.data[n] = self.data[n].replace('\n', '')
            return

        if q == 'w':
            # 'a'代表是append追加，不然会覆盖
            self.f = open(path, 'a', encoding=conding)
            return

        if q == 'rw':
            for line in open(path, encoding=conding):
                self.data.append(line)

            # 将末尾换行符替换
            for n in range(self.data.__len__()):
                # 处理非法字符
                self.data[n] = self.data[n].encode('utf-8').decode('utf-8-sig')
                self.data[n] = self.data[n].replace('\n', '')
            # 写入
            self.f = open(path, 'a', encoding=conding)
            return

    def read(self):
        return self.data

    def write(self, connet):
        # 如果打开失败
        if self.f is None:
            logger.error('error:txt文件打开时失败！')
            return
        self.f.write(str(connet))

    def save_close(self):
        if self.f is None:
            logger.error('error:txt文件打开时失败！')
            return

        self.f.close()


if __name__ == '__main__':
    # write = Confrw('../lib/conf/conf.txt', q='w')
    # write.write('test123 \n')
    # write.save_close()

    read = Confrw('../lib/conf/conf.txt')
    text = read.read()
    print(text)
