# coding:utf8
from comment import config
from comment.confrw import Confrw
import pymysql
from comment import logger



class Mysqlinit:

    # 处理数据库配置文件
    def __init__(self, confpath):
        self.conf = {}
        configdict = config.getconfig(confpath)
        configdict['mysqlport'] = int(configdict['mysqlport'])
        self.conf =configdict

    # 处理SQL备份文件为SQL语句
    def red_sql_list(self, filepath):
        sql_list = []
        sqld = Confrw(filepath)
        sqldate =sqld.read()
        for sqlline in sqldate:
            if sqlline.startswith("DROP"):
                sql_list.append(sqlline.replace('DROP', "TRUNCATE").replace("IF EXISTS", ''))

            if sqlline.startswith("INSERT"):
                sql_list.append(sqlline)

        return sql_list

    # 初始化数据库配置
    def init_mysql(self, sqlpath):
        # 创建数据库连接
        mysqlconnect = pymysql.connect(user=self.conf['mysqluser'],
                                       password=self.conf['mysqlpassword'],
                                       port=self.conf['mysqlport'],
                                       host=self.conf['mysqlhost'],
                                       db=self.conf['mysqldb'],
                                       charset=self.conf['mysqlcharset']
                                       )
        # 获取游标
        youbiao =mysqlconnect.cursor()
        logger.info('%s数据正在恢复中。。。。' % sqlpath)

        # 执行sql
        for sql in self.red_sql_list(sqlpath):
            print(sql)
            youbiao.execute(sql)
            mysqlconnect.commit()
        youbiao.close()
        mysqlconnect.close()


if __name__ == '__main__':
    # sqllist = Mysqlinit.red_sql_list('D:\\MyToolsdocs\\userinfo.sql')
    # print(sqllist)
    initsql= Mysqlinit('../lib/conf/conf.txt')
    print(initsql.conf)
    initsql.init_mysql('D:\\MyToolsdocs\\userinfo.sql')


