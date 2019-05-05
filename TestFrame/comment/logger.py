# coding:utf8
import logging

#相对于test.py路径能找到对应的当前路径，如果使用命令运行（D:\PycharmProjects\TestFrame>python .\test.py D:\PycharmProjects\TestFrame\lib\cases\app用例.xls）改path = '.'
# 若在当前测试代码需要修改为‘..’
path = '.'
logger = None
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
handler = logging.FileHandler(path+"/lib/logs/all.log", encoding='utf8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 打印debug级别的日志
def debug(ss):
    global logger
    try:
        logger.debug(ss)
    except:
        return

# 打印debug级别的日志
def info(str):
    global logger
    try:
        logger.info(str)
    except:
        return

# 打印debug级别的日志
def warn(ss):
    global logger
    try:
        logger.warning(ss)
    except:
        return

# 打印error级别的日志
def error(ss):
    global logger
    try:
        logger.error(ss)
    except:
        return

# 打印debug级别的日志
def exception(e):
    global logger
    try:
        logger.exception(e)
    except:
        return


# 调试
if __name__ == '__main__':
    debug('test')
    info('test')
    warn('test')
    error('test')
    exception('test')
