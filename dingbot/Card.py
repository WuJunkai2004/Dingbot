# coding=utf-8

__version__ = '0.01.0'
__all__ = []

try:
    import urllib2 as _u
except ImportError:
    import urllib.request as _u

import json
import re
import sys

urlopen = _u.urlopen
request = _u.Request

user = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Mobile Safari/537.36'
head = {'User-Agent': user}

def _http_manage(url,data,headers):
    'Responsible for network access'
    text = urlopen(request(url,data,headers)).read()
    text = text.decode('utf-8') if(sys.version_info.major==3)else text
    return text

def _http_get(url,headers):
    'Inherited from _http_manage and responsible for network get'
    return _http_manage(url,None,headers)

def _http_post(url,data,headers):
    'Inherited from _http_manage and responsible for network get'
    return _http_manage(url,data,headers)

def _search(reg, string):
    try:
        return re.search(reg, string).group()
    except BaseException as e:
        return str(e)

def NewCard(msg):
    if  (msg.lower() == 'link'):
        return LinkCard
    elif(msg.lower() == 'markdown'):
        return MarkCard()
    elif(msg.lower() == 'action'):
        return ActionCard()
    elif(msg.lower() == 'feed'):
        return FeedCard()
    raise AttributeError(msg)

class BaseCard(dict):
    __leng__ = 0
    __attr__ = []
    __must__ = []
    def __call__(self):
        if(not self.check()):
            return 
        data = [ ( item, getattr(self,item) ) for item in self.__attr__ ]
        data = dict(data)
        return data

    def check(self):
        have = [ self.__must__[item] == False or hasattr( self, self.__attr__[item] ) for item in range(self.__leng__) ]
        return False not in have

class LinkCard(BaseCard):
    __leng__ = 4
    __attr__ = ['text', 'title', 'messageURL', 'picURL']
    __must__ = [True  , True   , True        , False   ]
    def auto(self):
        if(not hasattr(self,'messageURL')):
            raise AttributeError
        html = _http_get(self.messageURL , head)
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
