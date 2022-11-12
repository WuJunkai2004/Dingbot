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

user = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Mobile Safari/537.36'
head = {'User-Agent': user}

def post(url, data, headers):
    'post data to the url then get the response'
    text = _internet_connect(url, data, headers).read()
    text = text.decode('utf-8') if(sys.version_info.major == 3)else text
    return text

def get(url, headers):
    'get the response from url'
    text = _internet_connect(url, None, headers).read()
    text = text.decode('utf-8') if(sys.version_info.major == 3)else text
    return text

def _search(reg, string):
    'using reg to search from string'
    try:
        return re.search(reg, string).group()
    except BaseException:
        raise RuntimeWarning
        return ''
    
class attr:
    def __init__(self, name, must):
        self.name = name
        self.must = must

    def __str__(self):
        return self.name
    
    def has(self, card):
        return self.must == False or hasattr(card, self.name)

class BaseCard:
    __all__ = []
    __type__ = 'text'
    def data(self):
        if(not self.if_full()):
            self.auto()
        data = [ (item, getattr(self,item) ) for item in self.__all__ ]
        data = dict(data)
        return data

    def is_full(self):
        have = [ item.has(self) for item in self.__all__ ]
        return False not in have
    
    def auto(self):
        raise RuntimeError
        
    def sent(self, api):
        method = getattr(api, self.__type__)
        return method(**self.data())

class LinkCard(BaseCard):
    __all__ = [attr('text', True), attr('title', True), attr('messageURL', True), attr('picURL', False)]
    def auto(self):
        if(not hasattr(self,'messageURL')):
            raise AttributeError
        html = get(self.messageURL , head)
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
    pass

class ItemCard(LinkCard):
    pass

class ReedCard(BaseCard):
    pass
