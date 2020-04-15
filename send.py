# coding=utf-8

from urllib import quote_plus as plus
from base64 import b64encode as base
from urllib2 import urlopen as post
from urllib2 import Request as seal
from urllib2 import urlopen as get
from hashlib import sha256 as sha
from json import dumps as json
from time import time
from hmac import new


with open('config.json','r') as fin:
    url,secret=eval(fin.read())

def urls():
    '获取url'
    timestamp          = long(round(time() * 1000))
    secret_enc         = bytes(secret).encode('utf-8')
    string_to_sign     = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = bytes(string_to_sign).encode('utf-8')
    hmac_code          = new(secret_enc, string_to_sign_enc, digestmod=sha).digest()
    sign               = plus(base(hmac_code))
    return url+'&timestamp=%s&sign=%s'%(timestamp,sign)

def send(msg):
    '发送消息'
    requ=seal(urls(),data=json(msg),headers={'Content-Type': 'application/json' })
    print eval(post(requ).read())


def text(message,at=[]):
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
    return send(msg)


def link(title,text,url,pic=''):
    msg={
        'msgtype':"link",
        'link'   :{
            'title':title,
            'text' :text,
            'messageUrl':url,
            'picUrl'    :pic
            }
        }
    return send(msg)

def markdown(title,text,at=[]):
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
    return send(msg)

def push(title,text,*button):
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
    send(msg)

def feed():
    pass
