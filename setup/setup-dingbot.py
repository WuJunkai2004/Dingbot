from distutils.core import setup
import sys
import dingbot

try:
    readme = open('README').read()
except:
    readme = open('README',encoding='utf-8').read()


try:
    kw = {
        "name": 'Dingbot',
        "version": dingbot.__version__,
        "description": 'Dingtalk group\'s robot API Python SDK ( Simple )',
        "long_description": readme,
        "author": 'WuJunkai',
        "author_email": 'wujunkai20041123@outlook.com',
        "url": 'https://github.com/WuJunkai2004/Dingbot',
        "download_url": 'https://github.com/WuJunkai2004/Dingbot',
        'include_package_data':True,
        'package_data':{
            'dingbot':["__init__.py"]
        },
        'packages':[],
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
