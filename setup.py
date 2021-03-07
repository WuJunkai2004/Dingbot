from distutils.core import setup

import dingbot

try:
    readme = open('README.md').read()
except:
    readme = open('README.md',encoding='utf-8').read()

kw = {
    "name": 'DingRobotPy',
    "version": dingbot.__version__,
    "description": 'Dingtalk group\'s robot API Python SDK',
    "long_description": readme,
    "author": 'WuJunkai',
    "author_email": 'wujunkai20041123@outlook.com',
    "url": 'https://github.com/WuJunkai2004/Dingbot',
    "download_url": 'https://github.com/WuJunkai2004/Dingbo',
    "py_modules": ['dingbot'],
    "classifiers": [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: MIT License (MIT License)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
}

setup(**kw)
