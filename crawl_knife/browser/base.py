"""
图片拦截器
广告拦截器
"""


def image_interceptor(request):
    """
    Block PNG, JPEG, GIF And ICO images
    :param request:
    :return:
    """
    if request.path.endswith(('.png', '.jpg', '.gif', '.ico')):
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
