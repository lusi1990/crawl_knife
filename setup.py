#!/usr/bin/env python

from distutils.core import setup

setup(
    name='crawl_knife',
    version='0.1.6',
    description='Python crawl tool',
    author='Master',
    author_email='lusi2114@gmail.com',
    url='https://github.com/lusi1990/crawl_knife',
    install_requires=[
        "selenium>=4.0",
        "selenium-wire>=4.6.4",
        "requests>=2.27.1",
        "webdriver-manager>=3.7.0",
        "undetected-chromedriver==3.1.5.post4",
        "2captcha-python",
        "pydub",
        "SpeechRecognition",
    ],
    packages=['crawl_knife'],
    include_package_data=True,
    package_data={
        'crawl_knife': [
            './browser/add_ons/*',
            './browser/js/*',
            './browser/*',
            './captcha/*',
        ],
    },
    python_requires='>=3.6,<4',
    long_description_content_type="text/x-rst",
)
