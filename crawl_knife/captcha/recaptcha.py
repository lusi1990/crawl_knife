"""
解决 recaptcha
"""
import logging
import os
import tempfile
from urllib.parse import parse_qs
from urllib.request import urlretrieve

import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha

logger = logging.getLogger(__name__)


def solve_by_2captcha(driver: WebDriver, api_key, url, invisible=0):
    """
    使用 2captcha 解决 recaptcha
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


def solve_by_buster(driver: WebDriver):
    """
    通过 扩展插件 buster 解决
    :param driver:
    :return:
    """


def solve_by_speed_recognition(driver: WebDriver) -> bool:
    """
    通过 语音识别 SpeechRecognition
    :param driver:
    :return: 是否成功
    """
    #  check recaptcha is load? click recaptcha, aideo check,
    result = False
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "span#recaptcha-anchor"))).click()
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[contains(title,'recaptcha challenge expires in two minutes')]")))
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button#recaptcha-audio-button"))).click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".rc-audiochallenge-play-button button")))
        src = driver.find_element(By.ID, "audio-source").get_attribute("src")
        print(src)
        # get the mp3 audio file
        with tempfile.TemporaryFile() as fp:
            import speech_recognition
            from pydub import AudioSegment
            requests.get(src, headers={})
            f = urlretrieve(src, "src.mp3")
            dst = 'test.wav'
            sound = AudioSegment.from_mp3(fp)
            sound.export(dst, format='wav')
            # todo 测试 https://alphacephei.com/vosk/
            r = speech_recognition.Recognizer()
            with speech_recognition.AudioFile(dst) as source:
                audio_data = r.record(source)
                text = r.recognize_google(audio_data)

            if os.path.exists(dst):
                os.remove(dst)

        driver.switch_to.default_content()

        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe[name^='c-'][src^='https://www.google.com/recaptcha/api2/bframe?']")))
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="audio-response"]'))).send_keys(text)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="recaptcha-verify-button"]'))).click()
        driver.switch_to.default_content()
        result = True
    except Exception as err:
        import traceback
        traceback.print_exc()
    return result


def solve_by_vosk(driver: WebDriver, ):
    """
    通过 yolo 解决
    :param driver:
    :return:
    """


def solve_by_yolov5(driver: WebDriver):
    """
    通过 yolo 解决
    :param driver:
    :return:
    """
