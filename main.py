from user import id, password, line_notify_url, token
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import requests

class LineNotify:
    def __init__(self, url: str, token: str) -> None:
        self.url = url
        self.header = {'Authorization': 'Bearer ' + token}

    def send_msg(self, msg: str) -> None:
        data = {'message': msg}
        requests.post(self.url, headers=self.header, data=data)

def init_driver(url: str) -> uc.Chrome:
    driver = uc.Chrome(version_main=106)
    driver.get(url)
    return driver


def do_login(driver: uc.Chrome) -> None:
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="id"]')
        )
    )
    driver.find_element(By.XPATH, '//*[@id="id"]').send_keys(id)
    driver.find_element(By.XPATH, '//*[@id="pw"]').send_keys(password)
    driver.find_element(
        By.XPATH, '//*[@id="memberLoginForm"]/fieldset/div/p[3]/button').click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="contents"]/article/div/dl/dd[2]/a')
        )
    )


def do_carted(driver: uc.Chrome, url: str):
    driver.get(url)

    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="lecture_registration_button"]')
            )
        )
    except Exception as e:
        print("Sold out", e)
        return

    driver.find_element(
        By.XPATH, '//*[@id="lecture_registration_button"]').click()
    driver.find_element(
        By.XPATH, '//*[@id="popup_reg"]/div[2]/p[3]/button').click()

    time.sleep(1)

    if EC.alert_is_present():
        result = driver.switch_to.alert()
        result.accept()
    else:
        print("no alert")
        return

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH,
                    '//*[@id="contents"]/article/div/div/div[3]/a[3]')
            )
        )
    except:
        print("TIMEOUT")
    else:
        # send
        print('try ~ else')
        pass




if __name__ == '__main__':
    path = "/home/bgyoo/chrome/106.0.5249.61/chromedriver"
    url = "https://sports.idongjak.or.kr/home/12"

    url_list = [
        'https://sports.idongjak.or.kr/home/171?category2=ALL&comcd=DONGJAK06&center=DONGJAK06&category1=02&action=read&class_cd=00792&item_cd=I000224',  # 그룹 월수 20:30~21:50
        'https://sports.idongjak.or.kr/home/171?category2=ALL&comcd=DONGJAK06&center=DONGJAK06&category1=02&action=read&class_cd=00009&item_cd=I000010',  # 개인 월수/20:30~21:50
        'https://sports.idongjak.or.kr/home/171?category2=ALL&comcd=DONGJAK06&center=DONGJAK06&category1=02&action=read&class_cd=00280&item_cd=I000010',  # 개인 화목/20:00~20:50
        'https://sports.idongjak.or.kr/home/171?category2=ALL&comcd=DONGJAK06&center=DONGJAK06&category1=02&action=read&class_cd=00787&item_cd=I000010',  # 개인 화목/21:00~21:50

    ]

    driver = init_driver(url)
    notify = LineNotify(line_notify_url, token)
    notify.send_msg('Hello World')
    do_login(driver)
    while True:
        for url in url_list:
            do_carted(driver, url)
            time.sleep(1)
        time.sleep(60*10)
