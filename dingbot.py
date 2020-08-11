# coding=utf-8

# * A SDK for group robots of Dingtalk ( copyright )
# * Wu Junkai wrote by python 3.7.7
# * version = 3.00.0

__all__ = ['Dingapi','DingManage']

try:
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib  import quote_plus
except ImportError:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.parse   import quote_plus

import base64
import hashlib
import hmac
import json
import sys
import time

def _http_manage(url,data,headers):
    'Responsible for network access'
    text=urlopen(request(url,data,headers)).read()
    if(sys.version_info.major==3):
        text = text.decode('utf-8')
    return text

def _http_get(url,headers):
    'Inherited from _http_manage and responsible for network get'
    return _http_manage(url,None,headers)

def _http_post(url,data,headers):
    'Inherited from _http_manage and responsible for network get'
    return _http_manage(url,data,headers)

class _configure_manage:
    'Configuration file read and manage'
    def __init__(self,path=r'.\config.json'):
        self.path=path
        self.load()

    def load(self):
        try:
            fin=open(self.path,'r')
        except IOError:
            self.data={'names':[],'robot':[]}
        else:
            self.data=json.load(fin)
            fin.close()
    
    def save(self):
        with open(self.path,'w') as fout:
            json.dump(self.data,fout)

class _dingtalk_robot_signature:
    'dingtalk robot signature algorithm'
    def _python_2_signature(self,webhook,secret):
        timestamp          = long(round(time.time() * 1000))
        secret_enc         = bytes(secret).encode('utf-8')
        string_to_sign     = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = bytes(string_to_sign).encode('utf-8')
        hmac_code          = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign               = quote_plus(base64.b64encode(hmac_code))
        return '{}&timestamp={}&sign={}'.format(webhook,timestamp,sign)

    def _python_3_signature(self,webhook,secret):
        timestamp          = str(round(time.time() * 1000))
        secret_enc         = secret.encode('utf-8')
        string_to_sign     = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code          = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign               = quote_plus(base64.b64encode(hmac_code))
        return '{}&timestamp={}&sign={}'.format(webhook,timestamp,sign)
        
class _dingtalk_robot_manage(_dingtalk_robot_signature):
    'dingtalk robot manage , inherited from _dingbot_robot_signature'
    def __init__(self,mothed=['Signature']):
        self.mothed  = mothed
        self.conf    = _configure_manage()
        self.is_login = False

    def login(self,name=None,webhook=None,secret=None):
        self.is_login = True
        if(name in self.conf.data[u'names']):
            index=self.conf.data[u'names'].index(name)
            self.name    = self.conf.data[u'robot'][index][u'name']
            self.webhook = self.conf.data[u'robot'][index][u'webhook']
            self.secret  = self.conf.data[u'robot'][index][u'secret']
        else:
            self.name    = name
            self.webhook = webhook
            self.secret  = secret

    def remember(self):
        data={u'name':self.name,u'webhook':self.webhook,u'secret':self.secret}
        if(self.name in self.conf.data[u'names']):
            index=self.conf.data[u'names'].index(self.name)
            self.conf.data[u'robot'][index]=data
        else:
            self.conf.data[u'robot'].append(data)
        self.conf.save()

    def delete(self):
        if(self.name not in self.conf.data[u'names']):
            raise RuntimeError('{} is not a robot\'s name'.format(self.name))
        index=self.conf.data[u'names'].index(self.name)
        del self.conf.data[u'names'][index]
        del self.conf.data[u'robot'][index]
        self.conf.save()
        _dingtalk_robot_manage.__init__(self,None)

    def url(self):
        if('Signature' in self.mothed):
            signature_name   = '_python_{}_signature'.format(sys.version_info.major)
            signature_mothed = getattr(self,signature_name)
            return signature_mothed(self.webhook,self.secret)
        return self.webhook

    def __getattr__(self,text):
        if(text=='api' and self.is_login):
            return _dingtalk_robot_api(self)
        if(not self.is_login):
            raise RuntimeError("The robot must be logged in at first")
        raise AttributeError("'DingManage' object has no attribute '{}'".format(text))

    def __dir__(self):
        return ['api','delete','login','remember']

class DingManage(_dingtalk_robot_manage):
    ...

class _dingtalk_robot_api:
    'dingtalk robot api for controlling'
    def __init__(self,robot):
        self.__robot__= robot
        self.__api__  = None
        self.__at__   = None

    def __getattr__(self,mothed):
        self.__api__ = mothed
        return self.__post__

    def __post__(self,**kwattr):
        url     = self.__robot__.url()
        headers = {'Content-Type': 'application/json'}
        data    = json.dumps({'at':self.__at__,'msgtype':self.__api__,self.__api__:kwattr}).encode("utf-8")
        post    = _http_post( url, data, headers )
        self.__init__(self.__robot__)
        return eval(post)

    def at(self,**kwattr):
        self.__at__ = kwattr

    def __dir__(self):
        return ['ActionCard','FeedCard','at','link','markdown','text']

class Dingapi(_dingtalk_robot_api):
    ...
