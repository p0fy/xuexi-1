from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests, re, time, json, random
import win32gui, win32con

option = webdriver.ChromeOptions()
option.add_argument('disable-infobars')
# option.add_argument('headless')
driver = webdriver.Chrome(chrome_options=option)
driver.maximize_window()


def get_hardnews():
    '''获取重要新闻的网址列表的函数'''
    url = 'https://www.xuexi.cn/98d5ae483720f701144e4dabf99a4a34/data5957f69bffab66811b99940516ec8784.js'
    response = requests.get(url)

    data = response.text
    urls = re.findall('"static_page_url":"(.*?)"', data)
    return urls


# 获取第一频道网址列表
def get_video():
    # url = 'https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/datadb086044562a57b441c24f2af1c8e101.js'
    # response = requests.get(url)

    with open('第一频道.txt', 'r', encoding='utf-8') as f:
        data = f.read()
        urls = re.findall('"static_page_url":"(.*?)"', data)
        return urls


# 打开登录网址，等待30秒，扫描二维码后登录
def login():
    driver.get('https://pc.xuexi.cn/points/login.html')
    # driver.switch_to.window(handles[0])
    driver.find_element_by_css_selector('body').send_keys(Keys.END)
    time.sleep(20)


def get_info():
    '''获取积分信息
    参数：
    ruleid为返回积分类型的id
    ruleid=0 返回阅读文章积分
    ruleid=1 返回观看视频积分
    ruleid=9 返回文章时长积分
    ruleid=11 返回视频时长积分
    返回值：
    currentscore 为当前积分
    daymaxscore 为当天最大积分'''
    driver.get('https://pc-api.xuexi.cn/open/api/score/today/queryrate')
    data = driver.page_source
    data = re.findall('{"data":(.*?),"message"', data)
    info = json.loads(data[0])
    return info


# 登录系统
login()

doc_urls = get_hardnews()
video_urls = get_video()
rect = driver.get_window_rect()
h = (rect['height'] - 100) / 2
w = rect['width'] / 6
x, y = 0, 100
for i in range(6):
    top = y
    left = x + w * i
    index = random.randint(0, len(doc_urls) - 1)
    driver.execute_script(
        'window.open("{}", "_blank","top={},left={},width={},height={},alwaysRaised=yes,z-look=yes")'.format(
            doc_urls[index], top, left, 240, 300))
for i in range(6):
    top = y + h
    left = x + w * i
    index = random.randint(0, len(video_urls) - 1)
    driver.execute_script(
        'window.open("{}", "_blank","top={},left={},width={},height={},alwaysRaised=yes,z-look=yes")'.format(
            video_urls[index], top, left, 240, 300))
time.sleep(30)
handles = driver.window_handles
driver.switch_to.window(handles[0])
driver.get('https://pc-api.xuexi.cn/open/api/score/today/queryrate')

for i, hand in enumerate(handles):
    if i != 0:
        driver.switch_to.window(hand)
        title = driver.title
        print('窗口索引号：{}，学习内容：{}'.format(i, title))
        hwnd = win32gui.FindWindow('Chrome_WidgetWin_1', title + ' - Google Chrome')
        win32gui.SetWindowText(hwnd, '学习窗口：' + str(i))
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_HIDEWINDOW | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
        if i >= 1 and i <= 6:
            try:
                video_play = driver.find_element_by_class_name('outter')
            except:
                isvideo = False
                while isvideo == False:
                    print('\t提示：此学习内容非视频，不计视频积分，重新选择一个学习！')
                    index = random.randint(0, len(video_urls) - 1)
                    driver.get(video_urls[index])
                    title = driver.title
                    print('窗口索引号：{}，学习内容：{}'.format(i, title))
                    try:
                        video_play = driver.find_element_by_class_name('outter')
                    except:
                        isvideo = False
                    else:
                        video_play.click()
                        isvideo = True
            else:
                video_play.click()
        else:
            driver.find_element_by_css_selector('body').send_keys(Keys.PAGE_DOWN)
            driver.find_element_by_css_selector('body').send_keys(Keys.END)

while True:
    time.sleep(60)
    driver.switch_to.window(handles[0])
    infos = get_info()

    doc_current = infos[0]['currentScore']
    doc_day = infos[0]['dayMaxScore']
    print('阅读文章积分：已获{}分/上限{}分'.format(doc_current, doc_day))
    if doc_current != doc_day:
        index = random.randint(0, len(doc_urls) - 1)
        driver.switch_to.window(handles[7])
        driver.get(doc_urls[index])
        driver.find_element_by_css_selector('body').send_keys(Keys.PAGE_DOWN)
        driver.find_element_by_css_selector('body').send_keys(Keys.END)
        print('\t阅读文章积分不够，在第一行第六个窗口补学：{}'.format(driver.title))

    docs_current = infos[9]['currentScore']
    docs_day = infos[9]['dayMaxScore']
    print('文章学习时长积分：已获{}分/上限{}分'.format(docs_current, docs_day))

    video_current = infos[1]['currentScore']
    video_day = infos[1]['dayMaxScore']
    print('视频学习积分：已获{}分/上限{}分'.format(video_current, video_day))
    if video_current != video_day:
        driver.switch_to.window(handles[1])
        while True:
            index = random.randint(0, len(video_urls) - 1)
            driver.get(video_urls[index])
            try:
                video_play = driver.find_element_by_class_name('outter')
            except:
                pass
            else:
                video_play.click()
                break
        print('\t视频学习积分不够，在第二行第六个窗口补学：{}'.format(driver.title))

    videos_current = infos[11]['currentScore']
    videos_day = infos[11]['dayMaxScore']
    print('视频学习时长积分：已获{}分/上限{}分'.format(videos_current, videos_day))

    if doc_current == doc_day and docs_current == docs_day and video_current == video_day and videos_current == videos_day:
        print('------全部积分已修满------')
        break

driver.quit()
