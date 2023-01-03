# coding=utf-8

__version__ = '0.01.0'
__all__ = [ 'BaseCard',   #done
            'FeedCard', 
            'FileCard',
            'ImageCard', 
            'ItemCard', 
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

def _search(reg, string):
    'using reg to search from string'
    try:
        return re.search(reg, string).group()
    except BaseException:
        raise RuntimeWarning


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
    __all__  = []
    __type__ = ''
    def __init__(self, URI):
        self.uri = URI

    def __load__(self):
        raise RuntimeError('Can not run without any other change')

    def post(self):
        return self.__load__()

    def get(self):
        return self.__load__()

    def send(self,API):
        API.__api__ = self.__type__
        '''print(dict( zip(
            self.__all__,
            [self.__getattr__(item) for item in self.__all__]
        ) ))'''
        API.send( **dict( zip(
            self.__all__,
            [self.__getattr__(item) for item in self.__all__]
        ) ) )


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

        print({"title":title,"image":image,"text":text})


class ImageCard(BaseCard):
    __all__  = ['title', 'picURL']
    __type__ = 'markdown'
    def __load__(self):
        img = config()
        get_token = requests.post(img.data['image']['URL']+'token',
                                  json = {
                                    'username' : img.data['image']['username'],
                                    'password' : img.data['image']['password']
                                    })
        if(not get_token.json()['success']):
            raise DingError('get token unsuccess')
        else:
            token = get_token.json()['data']['json']

        print(token)



class ItemCard(LinkCard):
    __all__  = ['title', 'messageURL', 'picURL']
    __type__ = None
    def __load__(self):
        return super().__load__()


class FeedCard(BaseCard):
    __all__ = ['feeds']
    __type__ = 'feedCard'
    def __load__(self):
        return super().__load__()


class FileCard(BaseCard):
    __all__ = ['file','post_data','post_header']
    __type__ = 'link'