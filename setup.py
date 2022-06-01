#!/usr/bin/env python

from distutils.core import setup

setup(
    name='crawl_knife',
    version='0.0.7',
    description='Python crawl tool',
    author='Master',
    author_email='lusi2114@gmail.com',
    url='',
    install_requires=[
        "selenium>=3.141.0,<4.0",
        "selenium-wire>=4.6.4",
        "requests>=2.27.1",
        "webdriver-manager>=3.7.0",
    ],
    packages=['crawl_knife'],
    include_package_data=True,
    package_data={
        'crawl_knife': [
            './browser/add_ons/*',
            './browser/js/*',
        ],
    },
    python_requires='>=3.6,<4',
)
