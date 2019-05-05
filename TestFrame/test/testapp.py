# from keywords.appkeys import APP
# from appium import webdriver
import datetime


# app = APP(None)
#
# app.runappium('D:\\software\\Appium', '4723', 5)
# app.runapps('{ "platformName": "Android", "platformVersion": "6.0.1","deviceName": "127.0.0.1:7555","appPackage": "com.tencent.mm","appActivity": ".ui.LauncherUI","noReset": "true"}',5)
# app.sleep(10)
# # 点击搜索按钮
# #          //android.widget.FrameLayout[@content-desc="当前所在页面,与的聊天"]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.view.ViewGroup/android.support.v7.widget.LinearLayoutCompat/android.widget.RelativeLayout[1]
# app.click('//android.widget.FrameLayout[@content-desc="当前所在页面,与的聊天"]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/'
#         'android.view.ViewGroup/android.widget.FrameLayout[2]/android.view.ViewGroup/android.support.v7.widget.LinearLayoutCompat/android.widget.RelativeLayout[1]')
# # # 输入 订阅号
# app.back()
# # app.click('//android.widget.FrameLayout[@content-desc="当前所在页面,与的聊天"]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/'
#         'android.view.ViewGroup/android.widget.FrameLayout[2]/android.view.ViewGroup/android.support.v7.widget.LinearLayoutCompat/android.widget.RelativeLayout[1]')
# app.click('com.tencent.mm:id/kh')
# app.sendkeys('com.tencent.mm:id/kh','订阅号')
# # 点击搜索到的订阅号
# app.click('com.tencent.mm:id/py')



print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))