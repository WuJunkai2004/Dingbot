# coding=utf-8

# version=2.10.0

try:
    from urllib2 import urlopen as post
    from urllib2 import Request as seal
    from urllib2 import urlopen as get
    version=2
except ImportError:
    from urllib2.request import urlopen as post
    from urllib2.request import Request as seal
    from urllib2.request import urlopen as get
    version=3

from json import dumps as json

def _python2(self):
    ## python2 的加密算法
    from urllib import quote_plus as plus
    from base64 import b64encode as base
    from hashlib import sha256 as sha
    from time import time
    from hmac import new

    timestamp          = long(round(time() * 1000))
    secret_enc         = bytes(self.secret).encode('utf-8')
    string_to_sign     = '{}\n{}'.format(timestamp, self.secret)
    string_to_sign_enc = bytes(string_to_sign).encode('utf-8')
    hmac_code          = new(secret_enc, string_to_sign_enc, digestmod=sha).digest()
    sign               = plus(base(hmac_code))
    return self.url+'&timestamp=%s&sign=%s'%(timestamp,sign)


def _python3(self):
    ## python3 的加密算法
    from urllib.parse import quote_plus as plus
    from base64  import b64encode as base
    from hashlib import sha256 as sha
    from time import time
    from hmac import new

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
        self.url=_config[name]['webhook']
        self.secret=_config[name]['secret']
        if  (version==2):
            self.urls=_python2
        elif(version==3):
            self.urls=_python3

    def send(self,msg):
        '发送消息'
        requ=seal(self.urls(self),data=json(msg).encode("utf-8"),headers={'Content-Type': 'application/json' })
        recode=eval(post(requ).read())
        return recode

    def text(self,text,at=[]):
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
                "content":text
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

    def markdown(self,title,markdown,at=[]):
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
                "text" :markdown
                },
            "at"      :{
                "atMobiles":phone,
                "isAtAll"  :every
                }
            }
        return self.send(msg)

    def push(self,title,markdown,*button):
        '单条消息推送'
        btns=list(map(dict,map(lambda x:zip(('title','actionURL'),x),button)))
        if(len(btns)==1):
            ## 整体跳转ActionCard类型
            msg={
                "msgtype": "actionCard",
                'actionCard':{
                    'title':title,
                    'text' :markdown,
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
                    "text" : markdown,
                    "btns" : btns,
                    'btnOrientation':'0',
                    }
                }
        return self.send(msg)

    def feed(self,*links):
        '订阅推送'
        if(len(links)==1 and type(links[0])!=str):
            links=links[0]
        link=list(map(dict,map(lambda x:zip(('title','messageURL','picURL'),x),links)))
        msg={
            "msgtype":"feedCard",
            "feedCard":{
                'links':link
                }
            }
        return self.send(msg)

try:
    with open('config.json','r') as _fin:
        _config=eval(_fin.read())
except IOError:
    with open('config.json','w') as _fout:
        _fout.write('{}')
    _config={}

for _ in _config.keys():
    exec('%s=Dingbot("%s")'%(_,_))
