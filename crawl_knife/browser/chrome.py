import os
import sys

from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver.v2 as uc

from crawl_knife.browser.base import image_interceptor


def init_driver(user_agent=None,
                language: str = "en-US",
                proxy_uri: str = None,
                headless: bool = False,
                image_show: bool = True,
                resolution=None
                ):
    """
    初始化 chrome driver
    :param user_agent:
    :param language:
    :param proxy_uri: http://username:password@endpoint:port
    :param headless:
    :param image_show:
    :param resolution:
    :return:
    """
    wire_options = dict()
    if proxy_uri:
        wire_options["proxy"] = {
            "http": proxy_uri,
            "https": proxy_uri,
            'no_proxy': 'localhost,127.0.0.1'
        }
    wire_options['request_storage'] = 'memory',  # Store requests and responses in memory only
    wire_options['request_storage_max_size']: 100  # Store no more than 100 requests in memory

    chrome_options = webdriver.ChromeOptions()
    # TODO random resolution and user_agent
    if resolution:
        chrome_options.add_argument(f"--window-size={resolution}")
    if user_agent:
        chrome_options.add_argument(f"--user-agent={user_agent}")
    # 设置 语言为 英语
    chrome_options.add_argument(f"--lang={language}")

    prefs = {
        "profile.default_content_settings.popups": 0,  # 0 为屏蔽弹窗，1 为开启弹窗
        "profile.managed_default_content_settings.images": 1 if image_show else 2,
        "profile.password_manager_enabled": False,
        "credentials_enable_service": False,
    }
    chrome_options.add_experimental_option("prefs", prefs)  # 这是添加参数到 options里面
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-plugins")

    if sys.platform.upper().startswith("WIN"):
        chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    _root = os.path.abspath(os.path.dirname(__file__))
    chrome_options.headless = headless
    if not headless:
        chrome_options.add_extension(os.path.join(_root,
                                                  'add_ons', 'buster_captcha_solver_for_humans-1.3.1-chrome.zip'))
        chrome_options.add_extension(os.path.join(_root,
                                                  'add_ons', 'uBlock_Origin-1.42.4.crx'))
        chrome_options.add_extension(os.path.join(_root,
                                                  'add_ons', 'ipmjngkmngdcdpmgmiebdmfbkcecdndc-1.5.crx'))
    else:
        chrome_options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options,
                              seleniumwire_options=wire_options)
    with open(os.path.join(_root, 'js', 'stealth.min.js')) as f:
        js = f.read()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })

    return driver


def init_driver_uc(user_agent=None,
                   language: str = "en-US",
                   proxy_uri: str = None,
                   headless: bool = False,
                   version_main=None,
                   resolution=None
                   ):
    """
    初始化 chrome driver
    :param user_agent:
    :param language:
    :param proxy_uri: http://username:password@endpoint:port
    :param headless:
    :param version_main: chrome version
    :param resolution:
    :return:
    """
    wire_options = dict()
    if proxy_uri:
        wire_options["proxy"] = {
            "http": proxy_uri,
            "https": proxy_uri,
            'no_proxy': 'localhost,127.0.0.1'
        }
    wire_options['request_storage'] = 'memory',  # Store requests and responses in memory only
    wire_options['request_storage_max_size']: 100  # Store no more than 100 requests in memory

    chrome_options = webdriver.ChromeOptions()
    # if resolution:
    #     chrome_options.add_argument(f"--window-size={resolution}")
    # 设置 语言为 英语
    chrome_options.add_argument(f"--lang={language}")
    chrome_options.headless = headless

    driver = uc.Chrome(
        options=chrome_options,
        seleniumwire_options=wire_options,
        version_main=version_main,
    )

    return driver


if __name__ == '__main__':
    _driver = init_driver_uc(headless=False, resolution='1920,1080')
    try:
        # _driver.get('https://bot.sannysoft.com/')
        # _driver.get('https://cis.scc.virginia.gov/EntitySearch/Index')
        # _driver.get('https://www.google.com/recaptcha/api2/demo')
        # _driver.get('https://nowsecure.nl')
        # _driver.get('https://ecorp.sos.ga.gov')
        # import undetected_chromedriver.v2 as ucv2
        # _driver = ucv2.Chrome()
        print("before get ")
        _driver.get('https://ecorp.sos.ga.gov')
        import time

        print("get now")
        time.sleep(1000)
    except KeyboardInterrupt:
        pass
    finally:
        _driver.quit()
