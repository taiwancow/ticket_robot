#載入selenium模組
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains #移動畫面到指定位置
import os
import time
import ddddocr

concert=input("請輸入演唱會網址:")
user=input("請輸入帳號:")
password1=input("請輸入密碼:")
seat_num=input("請輸入位置名稱,ex:A1區、全票:")
# web=input("請輸入演唱會選擇座位的網址:")
ticket=input("請輸入購買的票數，ex:1,2,3...:")
ticket=int(ticket)
my_seat_num="//div[contains(text(), '"+seat_num+"')]"
#獲取當前文件路徑
path=os.path.dirname(__file__)
#設定chrome driver的執行檔路徑
options=Options()
options.chrome_executable_path=os.path.join(path, "chromedriver.exe")
#不關閉網頁
options.add_experimental_option("detach", True)
#建立driver物件實體，用程式操作瀏覽器運作
driver=webdriver.Chrome(options=options)
driver.maximize_window()
#連線到演唱會
driver.get(concert)
time.sleep(0.5)
#捲一格
driver.execute_script("window.scrollTo(0, 500);")

#點擊購票處
tickets = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'//span[@class="v-btn__content" and text()="立即購買" or text()="尚未開賣"]')))
tickets.click()
# #登入帳密
username=driver.find_element(By.XPATH, "//input[@placeholder='手機號碼 *']")
password=driver.find_element(By.XPATH, "//input[@autocomplete='new-password']")
username.send_keys(user)
password.send_keys(password1)
#登入
login=WebDriverWait(driver, 1, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,".nextBtn.mt-2.v-btn.v-btn--block.v-btn--has-bg.theme--light.v-size--x-large.white")))
login.send_keys(Keys.ENTER)
#點擊想要的座位
while True:
    try:
        while True:
            try:
                seat=WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located((By.XPATH, my_seat_num)))#每1秒刷新介面，直到元素出現，element_located為不管這個元素可否點擊
                seat.click()
                break
            except:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")#沒看到元素，就滾動往下滑

        #選擇幾位人數(預設4位)
        n=0
        while n<ticket:    
            people = WebDriverWait(driver,1,0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
                ".v-icon.notranslate.mdi.mdi-plus.theme--light.primary-1--text"))) #element_to_be_clickable為等到這個元素變得可點擊
            people.click()
            n+=1
        print("可以購買")
        break
    except:
            print("還不能購買，重新整理")
            driver.refresh()
            time.sleep(1)
#演唱會選擇座位的網址
web=driver.current_url
# print(web)
#捲動到底部
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
#獲取當前文件路徑
imgname="picture.png"
fullpath=os.path.join(path, imgname)
#截圖驗證碼
def screenshot():
    veritycode=WebDriverWait(driver, 2, 1).until(EC.presence_of_element_located((By.CLASS_NAME,"captcha-img")))
    time.sleep(1)
    veritycode.screenshot(fullpath)
# 用pytesseract辨識並輸入驗證碼
def veritycode():
    ocr = ddddocr.DdddOcr()
    f = open(fullpath, mode='rb')  # 轉成二進制讀取
    img = f.read()
    x = ocr.classification(img)
    return x
#判斷是否要重新輸入驗證碼
retry=True
while retry:
    #第一次截圖跟辨識並輸入驗證碼
    screenshot()
    result = veritycode()
    print(result)
    # 輸入驗證碼
    CAPTCHA = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='請輸入驗證碼']")))
    CAPTCHA.clear()
    CAPTCHA.send_keys(result)
    next_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH,'//span[@class="v-btn__content" and text()="下一步"]')))
    next_button.click()
    web_now=driver.current_url
    #如果頁面沒跳轉
    if web==web_now:
         retry=True#重新驗證
    else:
         retry=False#結束迴圈
