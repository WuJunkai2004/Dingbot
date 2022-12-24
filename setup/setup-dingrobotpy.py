from distutils.core import setup
import sys
import dingbot

try:
    readme = open('README').read()
except:
    readme = open('README',encoding='utf-8').read()

try:
    kw = {
        "name": 'DingRobotPy',
        "version": dingbot.__version__,
        "description": 'Dingtalk group\'s robot API Python SDK',
        "long_description": readme,
        "author": 'WuJunkai',
        "author_email": 'wujunkai20041123@outlook.com',
        "url": 'https://github.com/WuJunkai2004/Dingbot',
        "download_url": 'https://github.com/WuJunkai2004/Dingbot',
        'packages':['dingbot'],
        "classifiers": [
            'Development Status :: 5 - Production/Stable',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    }

    setup(**kw)
except:
    pass