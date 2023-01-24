__version__ = '0.04.0'
__all__ = [ 'BaseCard',   #debuging
            'FeedCard',   #debuging
            'FileCard',
            'ImageCard',  #done
            'ItemCard',   #done
            'LinkCard']   #done

from dingbot import config
from dingbot import DingError

import json
import re
import requests

import sys
import time

user = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42'
acce = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
head = {'User-Agent': user}

error_level = 1 # 1 is throw all of error, 
                # 0 is ingore all of error,
                # 2 is throw all of warming as error

def _error_log(string:str, is_error:bool = False, error_type = RuntimeError) -> None:
    if(error_level + is_error >= 2):
        raise error_type(string)
    elif(error_level):
        sys.stderr.write(str(string) + '\n')

def _search(reg, string):
    'using reg to search from string'
    try:
        return re.search(reg, string).group()
    except BaseException:
        _error_log('Can not search the RegExp in the string', True)
        return ''


class _Card(dict):
    def __getattr__(self, __name):
        try:
            return self.__dict__[__name]
        except KeyError as e:
            raise e
        
    def __setattr__(self, __name, __value):
        self.__dict__[__name] = __value


class BaseCard(_Card):
    __all__  = []
    __type__ = ''
    def __init__(self, URI):
        self.uri = URI
        self.data = {}

    def __load__(self):
        _error_log('Can not run without any other change', True)

    def __repr__(self) -> str:
        return str(dict(zip(self.__all__, [self.__getattr__(item) for item in self.__all__])))

    def __str__(self) -> str:
        return self.__repr__()

    def post(self):
        return self.__load__()

    def get(self):
        return self.__load__()

    def send(self,API):
        API.__api__ = self.__type__
        self.data = eval(repr(self))
        _error_log(self.data)
        return API.send(**self.data)


class LinkCard(BaseCard):
    __all__  = ['text', 'title', 'messageUrl', 'picUrl']
    __type__ = 'link'
    def __load__(self):
        self.messageUrl = self.uri
        html = requests.get(self.messageUrl , headers = head).text
        ## title
        title = _search(r'<title.+?title>',html)
        title = _search(r'(?<=>).+?(?=<)',title)
        self.title = title
        ## picURL
        image = _search(r'<img.+?src.+?>',html)
        image = _search(r'(?<=src=["\']).+?(?=["\'])',image)
        self.picUrl = image
        ## text
        text = self.messageUrl
        self.text = text
        _error_log({"title":title,"image":image,"text":text})


class ImageCard(BaseCard):
    __all__  = ['title', 'text']
    __type__ = 'markdown'
    def __load__(self):
        cfg = config()
        img = cfg.data['image']
        if('token' not in img.keys()):
            get_token = requests.post(  img['URL']+'token',
                                        data = {'username':img['username'], 'password':img['password']} )
            if(not get_token.json()['success']):
                raise DingError('get token unsuccess')
            else:
                token = get_token.json()['data']['token']
                cfg.data['image']['token'] = token
                cfg.save()
        else:
            token = img['token']
        headers = {'Authorization':token}
        files = {'smfile':open(self.uri,'rb'), 'format':'json'}
        post_img = requests.post(   img['URL']+'upload',
                                    files = files ,
                                    headers = headers   )
        if(not post_img.json()['success']):
            raise DingError('post image error')
        self.title = '[image]'
        self.text = '![]({})'.format(post_img.json()['data']['url'])


class ItemCard(LinkCard):
    __all__  = ['title', 'messageURL', 'picURL']
    __type__ = None
    def __load__(self):
        LinkCard.__load__(self)
        self.messageURL = self.messageUrl
        self.picURL     = self.picUrl


class FeedCard(BaseCard):
    __all__ = ['links']
    __type__ = 'feedCard'
    def __init__(self):
        BaseCard.__init__(self, '')

    def __load__(self):
        _error_log(self)


class FileCard(LinkCard):
    __all__  = ['text', 'title', 'messageUrl', 'picUrl']
    __type__ = 'link'
    def __load__(self):
        return super().__load__()