"""
图片拦截器
广告拦截器
"""
import json
import os
import tempfile

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

STATIC_END = ('.js', '.css', '.woff', '.woff2', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico')


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


def get_cache_path(request):
    """

    :param request:
    :return:
    """
    return os.path.join(tempfile.gettempdir(), 'selenium_cache', request.host)


def static_request_interceptor(request, block_google_api=True):
    """
    如果已经缓存了静态资源，则直接读缓存
    :param request:
    :param block_google_api: 是否屏蔽一些 google 服务， 比如 更新。。。
    :return:
    """
    if request.path.endswith('.ico'):
        request.abort()
    if block_google_api:
        if 'update.googleapis.com/service/update2' in request.url:
            request.abort()
        if 'accounts.google.com' in request.url:
            request.abort()
        if 'www.googleapis.com/chromewebstore/v1.1/items/verify' in request.url:
            request.abort()
    if request.path.endswith(STATIC_END):
        request.headers['Accept-Encoding'] = 'gzip'
        cache_home = get_cache_path(request)
        file_path = os.path.join(cache_home, request.path.strip('/')) + request.querystring
        if os.path.isfile(file_path):
            headers = json.load(open(file_path + "_headers", 'r', encoding='utf-8'))
            headers['X-Server'] = 'FILE_SERVER'
            body = open(file_path, 'rb').read()
            request.create_response(
                status_code=200,
                headers=headers,
                body=body
            )


def static_response_interceptor(request, response):
    """
    缓存静态资源: js, css, image, font
    和 static_request_interceptor 配合使用
    :param request:
    :param response:
    :return:
    """
    if response.headers.get('x-server', '') == 'FILE_SERVER':
        return
    if request.path.endswith(STATIC_END) and response.status_code == 200:
        path, name = os.path.split(request.path)
        cache_home = get_cache_path(request)
        cache_path = os.path.join(cache_home, path.strip('/'))
        # fixme filename maybe to long (MACOS MAX NAME is 255)
        # todo use pickle save response
        file_path = os.path.join(cache_path, name) + request.querystring
        if not os.path.isfile(file_path):
            if not os.path.isdir(cache_path):
                os.makedirs(cache_path)
            with open(file_path, 'wb', ) as f:
                body = response.body
                if response.headers.get('content-encoding', '').lower() == 'br':
                    import brotli
                    body = brotli.decompress(response.body)
                elif response.headers.get('content-encoding', '').lower() == 'gzip':
                    import gzip
                    body = gzip.decompress(response.body)
                f.write(body)
            with open(file_path + "_headers", 'w', encoding='utf-8') as f:
                f.write(json.dumps(dict(response.headers)))


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
