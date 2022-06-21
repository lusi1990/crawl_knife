import os

from seleniumwire import webdriver

from webdriver_manager.firefox import GeckoDriverManager


def init_driver(user_agent=None,
                language: str = "en-US",
                proxy_uri: str = None,
                headless: bool = False,
                image_show: bool = True,
                resolution=None
                ):
    """
    todo 初始化 gecko driver
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
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

    firefox_options: webdriver.FirefoxOptions = webdriver.FirefoxOptions()
    if headless:
        firefox_options.add_argument(argument="-headless")
    # firefox_options.add_argument(argument="-kiosk")

    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_profile=firefox_profile,
                               options=firefox_options,
                               seleniumwire_options=wire_options)

    return driver


if __name__ == '__main__':
    _driver = init_driver(headless=False, image_show=True, resolution='1920,1080')
    try:
        _driver.get('https://bot.sannysoft.com/')
        # _driver.get('https://cis.scc.virginia.gov/EntitySearch/Index')
        # _driver.get('https://www.google.com/recaptcha/api2/demo')
        # _driver.get('https://nowsecure.nl')
        import time

        time.sleep(1000)
    except KeyboardInterrupt:
        pass
    finally:
        _driver.quit()
