# coding=utf-8

# version=2.10.0

try:
    from urllib2 import urlopen as _urlopen
    from urllib2 import Request as _request
    version=2
except ImportError:
    from urllib2.request import urlopen as _urlopen
    from urllib2.request import Request as _request
    version=3

from json import dumps as json
from json import loads as jsoff

get =lambda url,     headers={'User-Agent':'Mozilla/5.0'}       :_urlopen(_request(url,None,headers))
post=lambda url,data,headers={'Content-Type':'application/json'}:_urlopen(_request(url,data,headers))

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
    return self.hook+'&timestamp=%s&sign=%s'%(timestamp,sign)


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
    return self.hook+'&timestamp=%s&sign=%s'%(timestamp,sign)


class Dingbot(object):
    def __init__(self,webhook,secret=''):
        if(webhook in _config['names']):
            index=_config['names'].index(webhook)
            self.secret=_config['robot'][index]['secret']
            self.hook  =_config['robot'][index]['webhook']
        else:
            self.hook  =webhook
            self.secret=secret

        if  (version==2):
            self.urls=lambda:(_python2(self) if(self.secret)else self.hook)
        elif(version==3):
            self.urls=lambda:(_python3(self) if(self.secret)else self.hook)

    def save(self,name):
        if(name not in _config['names']):
            _config['names'].append(name)
            _config['robot'].append({'name':name,'secret':self.secret,'webhook':self.hook})
        else:
            index=_config['names'].index(name)
            _config['robot'][index]['secret'] =self.secret
            _config['robot'][index]['webhook']=self.hook
        fout=open('config.json','w')
        fout.write(json(_config))
        fout.close()

    def send(self,msg):
        '发送消息'
        recode=post(self.urls(),data=json(msg).encode("utf-8"))
        return eval(recode.read())

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
    _fin=open('config.json','r')
except IOError:
    _config={"names":[],"robot":[]}
else:
    _config=eval(_fin.read())
    _fin.close()
