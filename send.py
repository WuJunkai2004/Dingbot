# coding=utf-8

# version=2.00.0

import sys
version=sys.version_info.major

if  (version==2):
    from urllib import quote_plus as plus
    from urllib2 import urlopen as post
    from urllib2 import Request as seal
    from urllib2 import urlopen as get
elif(version==3):
    from urllib.parse import quote_plus as plus
    from urllib2.request import urlopen as post
    from urllib2.request import Request as seal
    from urllib2.request import urlopen as get

from base64 import b64encode as base
from hashlib import sha256 as sha
from json import dumps as json
from time import time
from hmac import new

def python2(self):
    ## python2 的加密算法
    timestamp          = long(round(time() * 1000))
    secret_enc         = bytes(self.secret).encode('utf-8')
    string_to_sign     = '{}\n{}'.format(timestamp, self.secret)
    string_to_sign_enc = bytes(string_to_sign).encode('utf-8')
    hmac_code          = new(secret_enc, string_to_sign_enc, digestmod=sha).digest()
    sign               = plus(base(hmac_code))
    return self.url+'&timestamp=%s&sign=%s'%(timestamp,sign)

def python3(self):
    ## python3 的加密算法
    timestamp          = str(round(time.time() * 1000))
    secret_enc         = secret.encode('utf-8')
    string_to_sign     = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code          = new(secret_enc, string_to_sign_enc, digestmod=sha).digest()
    sign               = plus(base64.b64encode(hmac_code))
    return self.url+'&timestamp=%s&sign=%s'%(timestamp,sign)


class Dingbot(object):

    def __init__(self,name):
        '初始化'
        self.name=name
        self.url=config[name]['webhook']
        self.secret=config[name]['secret']
        if  (version==2):
            self.urls=python2
        elif(version==3):
            self.urls=python3

    def send(self,msg):
        '发送消息'
        requ=seal(self.urls(self),data=json(msg).encode("utf-8"),headers={'Content-Type': 'application/json' })
        print eval(post(requ).read())


    def text(self,message,at=[]):
        '文本信息'
        phone=[]
        every=False
        if(at==all):
            every=True
        else:
            phone=map(str,at)
        msg={
            'msgtype':'text',
            'text'   :{
                "content":message
                },
            'at'     :{
                'atMobiles':phone,
                'isAtAll'  :every 
                }
            }
        return self.send(msg)


    def link(self,title,text,url,pic=''):
        '链接'
        msg={
            'msgtype':"link",
            'link'   :{
                'title':title,
                'text' :text,
                'messageUrl':url,
                'picUrl'    :pic
                }
            }
        return self.send(msg)

    def markdown(self,title,text,at=[]):
        'markdown'
        phone=[]
        every=False
        if(at==all):
            every=True
        else:
            phone=map(str,at)
        msg={
            "msgtype":"markdown",
            "markdown":{
                "title":title,
                "text" :text
                },
            "at"      :{
                "atMobiles":phone,
                "isAtAll"  :every
                }
            }
        return self.send(msg)

    def push(self,title,text,*button):
        '单条消息推送'
        btns=[]
        for i in map(dict,map(lambda x:zip(('title','actionURL'),x),button)):
            btns.append(i)
        if(len(btns)==1):
            ## 整体跳转ActionCard类型
            msg={
                "msgtype": "actionCard",
                'actionCard':{
                    'title':title,
                    'text' :text,
                    'btnOrientation':'0',
                    'singleTitle'   :btns[0]['title'],
                    'singleURL'     :btns[0]['actionURL'],
                    }
                }
        else:
            ## 独立跳转ActionCard类型
            msg={
                "msgtype": "actionCard",
                "actionCard": {
                    "title": title,
                    "text" : text,
                    "btns" : btns,
                    'btnOrientation':'0',
                    }
                }
        return self.send(msg)

    def feed(self,links):
        '订阅推送'
        pass



with open('config.json','r') as fin:
    config=eval(fin.read())

for i in config.keys():
    exec('%s=Dingbot("%s")'%(i,i))
