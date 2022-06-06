"""
解决 recaptcha
"""
import logging
from urllib.parse import parse_qs

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from twocaptcha import TwoCaptcha

logger = logging.getLogger(__name__)


def solve_by_2captcha(driver: WebDriver, api_key, url, invisible=0):
    """

    :param driver: selenium webdriver
    :param api_key: 2captcha api key
    :param url: url to solve
    :param invisible: 如果是隐藏的 recaptcha 设置成 1
    :return:
    """
    # 通过 www.google.com/recaptcha/api2/anchor 或者 data-sitekey 找到 k 的值,
    try:
        re_captcha_iframe = driver.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']")
    except NoSuchElementException:
        logger.error('reCaptcha 未找到')
        return False
    solver = TwoCaptcha(api_key)
    src = re_captcha_iframe.get_property('src')
    # 解析链接中的 k
    re_captcha_k = parse_qs(src)['k'][0]
    kwargs = dict()
    if invisible:
        kwargs['invisible'] = 1
    # 调用 2captcha 接口 得到 token
    try:
        result = solver.recaptcha(
            sitekey=re_captcha_k,
            url=url,
            lang='en',
            **kwargs
        )
    except Exception as err:
        logger.error('2captcha 过验证码失败, err:%s', err)
        return False
    logger.debug('solved: %s', result)
    token = result.get('code')
    if not token:
        logger.error('2captcha 过验证码失败, result:%s', result)
        return False

    # 将 token 放入 g-recaptcha-response 中
    try:
        driver.find_element(By.ID, 'g-recaptcha-response')
        driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML = "{token}";')
    except NoSuchElementException:
        driver.execute_script(f'document.getElementById("g-recaptcha-response-100000").innerHTML = "{token}";')
    return True


def solve_by_buster(driver):
    """
    通过 扩展插件 buster 解决
    :param driver:
    :return:
    """


def solve_by_speed_recognition(driver):
    """
    通过 语音识别 SpeechRecognition
    :param driver:
    :return:
    """


def solve_by_yolov5(driver):
    """
    通过 yolo 解决
    :param driver:
    :return:
    """
