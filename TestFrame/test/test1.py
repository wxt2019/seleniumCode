from keywords.webkeys import Web
from comment.Excelrw import Writer
import time

writer = Writer()

web = Web(writer)
# 浏览器类型
web.getwebdriver('cc')
# 打开网站
web.openurl('http://112.74.191.10:8000/')
web.click('/html/body/div[1]/div[1]/div/ul/li[1]/a')
# 切换窗口
web.to_windows(2)
# 登录
web.inputtext('//*[@id="username"]','13800138006')
web.inputtext('//*[@id="password"]','123456')
web.inputtext('//*[@id="verify_code"]','123456')
web.click('//*[@id="loginform"]/div/div[6]/a')
# 返回首页/html/body/div[2]/div/div[2]/a[2]   /html/body/div[2]/div/div[3]/ul/li[1]/a
# web.click('/html/body/div[2]/div/div[1]/a/img')
# 搜索商品//*[@id="q"]
web.inputtext('//*[@id="q"]', '手机')
web.click('//*[@id="sourch_form"]/a')
web.scoll(0,1300)
web.click('/html/body/div[4]/div/div[2]/div[2]/ul/li[5]/div/div[5]/div[2]/a')
web.in_iframe('//*[@id="layui-layer-iframe1"]')
web.asserequals('//*[@id="addCartBox"]/div[1]/div/span', '添加成功')
web.out_iframe()
web.hover('//*[@id="hd-my-cart"]/a/div')







