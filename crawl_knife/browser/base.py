"""
图片拦截器
广告拦截器
"""
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def image_interceptor(request):
    """
    Block PNG, JPEG, GIF And ICO images
    :param request:
    :return:
    """
    if request.path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico')):
        request.abort()


def ads_interceptor(request):
    """
    todo 广告拦截器
    :param request:
    :return:
    """


def locate():
    """

    :return:
    """


def send_keys(driver, words: str):
    """
    延时输入
    :return:
    """


def check_elem_exists(parent, by, selector, wait=False, timeout=False):
    """

    :param parent:
    :param by:
    :param selector:
    :param wait:
    :param timeout:
    :return:
    """
    if not wait:
        try:
            parent.find_element(by, selector)
        except NoSuchElementException:
            return False
        else:
            return True
    # when allowing wait time - print note for what is happening
    print('%s - check_elem_exists(%is..)' % (selector, timeout))
    try:
        WebDriverWait(parent, timeout).until(EC.presence_of_element_located((by, selector)))
    except NoSuchElementException:
        return False
    except TimeoutException:
        return False
    else:
        return True
