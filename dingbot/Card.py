# coding=utf-8

__version__ = '0.01.0'
__all__ = ['BaseCard', 'FeedCard', 'ImageCard', 'ItemCard', 'LinkCard']

try:
    from dingbot   import _internet_connect
except ImportError:
    from __init__  import _internet_connect

import json
import re
import sys
from tkinter import N
from turtle import title

user = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Mobile Safari/537.36'
head = {'User-Agent': user}

def _search(reg, string):
    'using reg to search from string'
    try:
        return re.search(reg, string).group()
    except BaseException:
        raise RuntimeWarning
        return ''

def _post(url, data, headers):
    'post data to the url then get the response'
    text = _internet_connect(url, data, headers).read()
    text = text.decode('utf-8') if(sys.version_info.major == 3)else text
    return text

def _get(url, headers):
    'get the response from url'
    text = _internet_connect(url, None, headers).read()
    text = text.decode('utf-8') if(sys.version_info.major == 3)else text
    return text

class _Card:
    __dict__ = {}
    def __getattr__(self, __name):
        try:
            return self.__dict__[__name]
        except KeyError:
            return ''
        
    def __setattr__(self, __name, __value):
        self.__dict__[__name] = __value

class BaseCard(_Card):
    'Base Card for dingbot'
    __all__  = []
    __type__ = ''
    __variable__ = {
        'required' : [],
        'optional' : []
    }
    def __init__(self):
        'Initialize basic data'
        for item in self.__all__:
            self.__dict__[item] = None
        self.__doc__ = ', '.join(self.__all__)
        
    def __call__(self, *args, **kwds):
        'Initialize and assign'
        for index in range(len(args)):
            self.__dict__[ self.__all__[index] ] = args[index]
        for index in kwds.keys():
            self.__dict__[index] = kwds[index]
    
    def _is_fill(self, __list):
        for item in __list:
            if(not self.__dict__[item]):
                return False
        return True
    
    def is_fill_necessary(self):
        return self._is_fill(self.__variable__['required'])

    def is_fill_all(self):
        return self._is_fill(self.__all__)
    
    def auto_fill(self):
        'auto fill if something did not be filled'
        raise RuntimeWarning('Need over')

    def data(self):
        'pack the data'
        if(not self.is_fill_all()):
            self.auto_fill()
        data = [ (item, getattr(self,item) ) for item in self.__all__ ]
        data = dict(data)
        return data

    def sent(self, api):
        'sent the data'
        method = getattr(api, self.__type__)
        return method(**self.data())

class LinkCard(BaseCard):
    __all__  = ['text', 'title', 'messageURL', 'picURL']
    __type__ = 'link'
    __variable__ = {
        'required' : ['messageURL']
    }
    def auto_fill(self):
        if(not self.is_fill_necessary()):
            raise AttributeError
        html = _get(self.messageURL , head)
        ## title
        title = _search(r'title.+?title',html)
        title = _search(r'(?<=>).+?(?=<)',title)
        self.title = title
        ## picURL
        image = _search(r'<img.+?src.+?>',html)
        image = _search(r'(?<=src=["\']).+?(?=["\'])',image)
        self.picURL = image
        ## text
        self.text = self.messageURL

class ImageCard(BaseCard):
    __all__  = ['title', 'picPATH', 'picURL']
    __type__ = 'markdown'
    __variable__ = {
        'required' : ['picURL']
    }
    def auto_fill(self):
        pass

    def data(self):
        if(not self.is_fill_all()):
            self.auto_fill()
        return {
            'title':title,
            'text' :'![]({})'.format(self.picURL)
        }

class ItemCard(LinkCard):
    pass

class FeedCard(BaseCard):
    pass
