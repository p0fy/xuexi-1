import time, json
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def get_userpwd():
    with open('userpwd.json','r') as f:
        userdict = json.load(f)
        user = userdict['user']
        password = userdict['password']
    return user, password


def login(user, password):
    WebDriverWait(driver, 20).until(
        lambda the_driver: the_driver.find_element_by_id('cn.xuexi.android:id/et_phone_input').is_displayed())
    driver.find_element_by_id('cn.xuexi.android:id/et_phone_input').send_keys(user)
    driver.find_element_by_id('cn.xuexi.android:id/et_pwd_login').send_keys(password)
    WebDriverWait(driver, 20).until(
        lambda the_driver: the_driver.find_element_by_id('cn.xuexi.android:id/btn_next').is_displayed())
    driver.find_element_by_id('cn.xuexi.android:id/btn_next').click()
    WebDriverWait(driver, 20).until(
        lambda the_driver: the_driver.find_element_by_accessibility_id('同意').is_displayed())
    driver.find_element_by_accessibility_id('同意').click()


def switch_tab(tab_index):
    '''切换选项卡'''
    if tab_index == 1:
        xpath = '//android.widget.FrameLayout[@content-desc="关注"]/android.widget.RelativeLayout'
        WebDriverWait(driver, 20).until(
            lambda the_driver: the_driver.find_element_by_xpath(xpath).is_displayed())
        driver.find_element_by_xpath(xpath).click()
    elif tab_index == 2:
        xpath = '//android.widget.FrameLayout[@content-desc="学习"]/android.widget.RelativeLayout'
        WebDriverWait(driver, 20).until(
            lambda the_driver: the_driver.find_element_by_xpath(xpath).is_displayed())
        driver.find_element_by_xpath(xpath).click()
    elif tab_index == 3:
        xpath = '//android.widget.FrameLayout[@content-desc="视频学习"]/android.widget.RelativeLayout'
        WebDriverWait(driver, 20).until(lambda the_driver: the_driver.find_element_by_xpath(xpath).is_displayed())
        driver.find_element_by_xpath(xpath).click()
    elif tab_index == 4:
        xpath = '//android.widget.FrameLayout[@content-desc="工作"]/android.widget.RelativeLayout'
        WebDriverWait(driver, 20).until(lambda the_driver: the_driver.find_element_by_xpath(xpath).is_displayed())
        driver.find_element_by_xpath(xpath).click()


def viewpoint(n=6):
    '''发表观点'''
    for i in range(n):
        xpath = '//android.widget.LinearLayout/android.widget.TextView[@text="欢迎发表你的观点"]'  # 发表观点的xpath
        WebDriverWait(driver, 20).until(
            lambda the_driver: the_driver.find_element_by_xpath(xpath).is_displayed())
        driver.find_element_by_xpath(xpath).click()
        WebDriverWait(driver, 20).until(
            lambda the_driver: the_driver.find_element_by_class_name('android.widget.EditText').is_displayed())
        driver.find_element_by_class_name('android.widget.EditText').send_keys('Learning power')
        xpath = '//android.widget.RelativeLayout/android.widget.TextView[@text="发布"]'
        WebDriverWait(driver, 20).until(
            lambda the_driver: the_driver.find_element_by_xpath(xpath).is_displayed())
        driver.find_element_by_xpath(xpath).click()
        xpath = '//android.widget.LinearLayout/android.widget.TextView[@text="删除"]'
        WebDriverWait(driver, 20).until(
            lambda the_driver: the_driver.find_element_by_xpath(xpath).is_displayed())
        driver.find_element_by_xpath(xpath).click()
        xpath = '//android.widget.LinearLayout/android.widget.Button[@text="确认"]'
        WebDriverWait(driver, 20).until(
            lambda the_driver: the_driver.find_element_by_xpath(xpath).is_displayed())
        driver.find_element_by_xpath(xpath).click()
        time.sleep(30)


def doc_collect():
    '''点击收藏，有弹出窗口，需处理'''
    try:
        xpath = '//android.widget.ImageView[@index=2]'  # 收藏图标的xpath
        WebDriverWait(driver, 20).until(
            lambda the_driver: the_driver.find_element_by_xpath(xpath).is_displayed())
        driver.find_element_by_xpath(xpath).click()
        time.sleep(3)
        WebDriverWait(driver, 20).until(
            lambda the_driver: the_driver.find_element_by_id(
                'cn.xuexi.android:id/btn_right_text').is_displayed())
        driver.find_element_by_id('cn.xuexi.android:id/btn_right_text').click()
    except:
        pass


def doc_share(n=6):
    '''分享到短信'''
    for i in range(n):
        xpath = '//android.widget.ImageView[@index=3]'  # 分享图标的xpath
        WebDriverWait(driver, 20).until(
            lambda the_driver: the_driver.find_element_by_xpath(xpath).is_displayed())
        driver.find_element_by_xpath(xpath).click()
        xpath = '//android.widget.GridView/android.widget.RelativeLayout[@index=4]'  # 分享到短信图标的xpath
        WebDriverWait(driver, 20).until(
            lambda the_driver: the_driver.find_element_by_xpath(xpath).is_displayed())
        driver.find_element_by_xpath(xpath).click()


desired_caps = {'platformName': 'Android',  # 平台名称
                'platformVersion': '5.1.1',  # 系统版本号
                'deviceName': '127.0.0.1:62001',  # 设备名称。如果是真机，在'设置->关于手机->设备名称'里查看
                'appPackage': 'cn.xuexi.android',  # apk的包名
                'appActivity': 'com.alibaba.android.rimet.biz.SplashActivity',  # activity 名称
                # 'unicodeKeyboard': True,  # 使用unicode编码方式发送字符串
                # 'resetKeyboard': True  # 将键盘隐藏起来
                }
driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)  # 连接Appium

if __name__ == '__main__':
    user, password = get_userpwd()
    login(user, password)
    switch_tab(1)  # 切换到关注
    n = 2
    for i in range(n):
        xpath = '//android.widget.ListView/android.widget.FrameLayout[@index={}]'.format(i + 1)  # 文章列表的xpath
        WebDriverWait(driver, 20).until(
            lambda the_driver: the_driver.find_element_by_xpath(
                xpath).is_displayed())
        driver.find_element_by_xpath(xpath).click()
        doc_collect()
        time.sleep(3)
        if i < n -1:
            driver.back()
            time.sleep(3)
    doc_share(2)
    viewpoint(2)
