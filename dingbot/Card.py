# coding=utf-8

__version__ = '0.01.0'
__all__ = ['BaseCard', 'FeedCard', 'FileCard', 'ImageCard', 'ItemCard', 'LinkCard']

try:
    from dingbot  import _internet_connect
except ImportError:
    from __init__ import _internet_connect

import json
import mimetypes
import re

import sys
import time

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


def _type(url):
    n = url.rfind('.')
    if n == -1:
        return 'application/octet-stream'
    ext = url[n:]
    return mimetypes.types_map.get(ext, 'application/octet-stream')


def _file(path):
    boundary = '----------%s' % hex(int(time.time() * 1000))
    with open(path) as fin:
        content  = fin.read()
        filename = getattr(fin, 'name', '')
    data = [
        '--{}'.format(boundary),
        'Content-Disposition: form-data; name="file"; filename="{}"'.format(path),
        'Content-Length: {}' .format( len(content) ),
        'Content-Type: {}\r\n' .format( _type(filename) ),
        content,
        '--{}--\r\n' .format( boundary )
    ]
    return '\r\n'.join(data), boundary

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
    __type__ = ''
    __variable__ = {
        'required' : [],'optional' : []
    }
    __all__ = __variable__['required'] + __variable__['optional']
    def __init__(self):
        'Initialize basic data'
        self.__doc__ = ', '.join(self.__all__)
        for item in self.__all__:
            self.__dict__[item] = None
        
    def __call__(self, *args, **kwds):
        'Initialize and assign'
        for index in range(len(args)):
            self.__dict__[ self.__all__[index] ] = args[index]
        for index in kwds.keys():
            self.__dict__[index] = kwds[index]
    
    def _is_fill(self, __list):
        'true if the list which was given is filled'
        for item in __list:
            if(not self.__dict__[item]):
                return False
        return True
    
    def is_fill_necessary(self):
        'true if the necessary are filled'
        return self._is_fill(self.__variable__['required'])

    def is_fill_all(self):
        'true if all of var are filled'
        return self._is_fill(self.__all__)

    def _fill(self):
        'using different ways to fill'
        raise RuntimeWarning('Need over')

    def _data(self):
        'using different ways to pack the data'
        data = [ (item, getattr(self,item) ) for item in self.__all__ ]
        return dict(data)
    
    def data_fill(self):
        'auto fill if something did not be filled'
        if(not self.is_fill_necessary()):
            raise AttributeError
        self._fill()
    
    def data_pack(self):
        'pack the data'
        if(not self.is_fill_all()):
            self.data_fill()
        return self._data()

    def data_send(self, api):
        'send the data'
        method = getattr(api, self.__type__)
        return method(**self.data())


class LinkCard(BaseCard):
    __type__ = 'link'
    __variable__ = {
        'required' : ['messageURL'],'optional':['text', 'title', 'picURL']
    }
    def _fill(self):
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
    __type__ = 'markdown'
    __variable__ = {
        'required' : ['file'],'optional':['text','picURL']
    }
    def _data(self):
        return {
            'title':self.title,
            'text' :'![]({})'.format(self.picURL)
        }

    def _fill(self):
        pass


class ItemCard(LinkCard):
    __type__ = None
    __variable__ = {
        'required' : ['messageURL'],'optional':['title', 'picURL']
    }
    def _data(self):
        return {
            'title' : self.title,
            'messageURL' : self.messageURL,
            'picURL' : self.picURL
        }


class FeedCard(BaseCard):
    __all__ = ['feeds']
    __type__ = 'feedCard'
    __variable__ = {'required' : ['feeds']}
    def _fill(self):
        for item in self.feeds:
            item.auto_fill()

    def _data(self):
        return {
            'links': [item.pack_data() for item in self.feeds]
        }

class FileCard(BaseCard):
    __type__ = 'link'
    __variable__ = {
        'required' : ['file'],'optional':['post_data', 'post_header','url']
    }
    def _fill(self):
        self.post_data , boundary = _file(self.file)
        self.post_header = {'User-Agent': 'curl/7.79.1','Accept': '*/*','Content-Type': 'multipart/form-data; boundary={}'.format(boundary)}
        content = _post('https://file.io/?maxDownloads=99',self.post_data,self.post_header)
        content = json.loads( content )
        if(content[u'success']):
            self.url = content[u'link']
        else:
            print(content)

    def _data(self):
        return {
            'title':self.file,
            'text':'文件',
            'messageURL':self.url
        }
        
        
