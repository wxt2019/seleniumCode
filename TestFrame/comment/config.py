# coding:utf8
from comment.confrw import Confrw
from comment import logger

config = {}

# 将list类型文件数据解析成dict类型
def getconfig(path):
    # 存放解析的数据
    global config
    config.clear()
    dd = Confrw(path)
    data = dd.read()
    print(data)
    # 逐行便利数据
    for s in data:
        if s.startswith("#"):
            continue

        if not s.find('=') > 0:
            logger.error('配置格式错误！' + str(s))

        try:
            key = s[0:s.find('=')]
            value = s[s.find('=') + 1:s.__len__()]
            config[key] = value
        except Exception as e:
            logger.error('排位置文件格式错误，请重新配置' + str(s))
            logger.exception(e)
    return config


# if __name__ == '__main__':
#     config = getconfig('../lib/conf/conf.txt')
#     print(config)
