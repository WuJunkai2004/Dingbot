# coding=utf-8

# * A SDK for group robots of Dingtalk ( copyright )
# * Wu Junkai wrote by python 3.7.7 , run in python 2.7.14 and python 3.8.1

__version__ = '3.40.0'
__all__ = ['Card', 'DingAPI', 'DingError', 'DingLimit', 'DingManage', 'DingRaise']

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
    text=urlopen(Request(url,data,headers)).read()
    if(sys.version_info.major==3):
        text = text.decode('utf-8')
    return text

def _http_get(url,headers):
    'Inherited from _http_manage and responsible for network get'
    return _http_manage(url,None,headers)

def _http_post(url,data,headers):
    'Inherited from _http_manage and responsible for network get'
    return _http_manage(url,data,headers)

def Card(**kwattr):
    'Changes values into dist'
    return kwattr

class _configure_manage:
    'Configuration file read and manage'
    def __init__(self,path=r'.\config.json'):
        self.path=path
        self.load()

    def load(self):
        try:
            with open(self.path,'r') as fin:
                self.data=json.load(fin)
        except IOError:
            self.data={'names':[],'robot':[]}

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
    __all__ = ['api', 'conf', 'delete', 'is_login', 'is_sign', 'login', 'name', 'remember', 'webhook']
    def __init__(self,name=None):
        self.conf     = _configure_manage()
        self.name     = name
        self.is_sign  = True
        self.is_login = False
        if(self.name in self.conf.data[u'names']):
            self.login()

    def login(self,webhook=None,secret=None):
        self.is_login = True
        self.webhook  = webhook
        self.secret   = secret
        if(self.name in self.conf.data[u'names']):
            index=self.conf.data[u'names'].index(self.name)
            self.webhook = self.conf.data[u'robot'][index][u'webhook']
            self.secret  = self.conf.data[u'robot'][index][u'secret']
        elif(not webhook):
            raise DingError('The robot need the webhook.')

    def remember(self):
        data={u'name':self.name,u'webhook':self.webhook,u'secret':self.secret}
        if(self.name in self.conf.data[u'names']):
            index=self.conf.data[u'names'].index(self.name)
            self.conf.data[u'robot'][index]=data
        else:
            self.conf.data[u'robot'].append(data)
            self.conf.data[u'names'].append(self.name)
        self.conf.save()

    def delete(self):
        if(self.name not in self.conf.data[u'names']):
            raise DingError('{} is not a robot\'s name'.format(self.name))
        index=self.conf.data[u'names'].index(self.name)
        del self.conf.data[u'names'][index]
        del self.conf.data[u'robot'][index]
        self.conf.save()
        _dingtalk_robot_manage.__init__(self,None)

    def url(self):
        if(self.is_sign):
            sign_mothed = getattr(self,'_python_{}_signature'.format(sys.version_info.major))
            return sign_mothed(self.webhook,self.secret)
        return self.webhook

    def __getattr__(self,text):
        if(text.lower()=='api' and self.is_login):
            return _dingtalk_robot_api(self)
        raise AttributeError("'_dingtalk_robot_manage' object has no attribute '{}'.".format(text))

class _dingtalk_robot_api:
    'dingtalk robot api for sending messages'
    __all__ = ['actionCard', 'at', 'feedCard', 'link', 'markdown', 'text']
    def __init__(self,robot):
        self.__robot__ = robot
        self.__api__   = None
        self.__at__    = None

    def __getattr__(self,mothed):
        self.__api__ = mothed
        return self.__post__

    def __post__(self,**kwattr):
        url     = self.__robot__.url()
        headers = {'Content-Type': 'application/json'}
        data    = json.dumps({'at':self.__at__,'msgtype':self.__api__,self.__api__:kwattr}).encode("utf-8")
        self.__init__(self.__robot__)
        return eval( _http_post( url, data, headers ) )

    def at(self,**kwattr):
        self.__at__ = kwattr

class _dingtalk_robot_within_limit(_dingtalk_robot_api):
    'inherited from _dingtalk_robot_api for judging lime limit'
    __history__={}
    def __contains__(self,value):
        if(self.__robot__.webhook not in self.__history__.keys()):
            self.__history__[self.__robot__.webhook] = [0] * 20
        return (value - self.__history__[self.__robot__.webhook][0] > 60 )

class DingError(RuntimeError):
    'dingtalk robot\'s error object'

class DingManage(_dingtalk_robot_manage):
    'inherited from _dingtalk_robot_manage'

class DingAPI(_dingtalk_robot_api):
    'inherited from _dingtalk_robot_api for sending messages'

class DingRaise(_dingtalk_robot_api):
    'inherited from _dingtalk_robot_api and raise error while sending messages wrong'
    def __post__(self,**kwattr):
        remsg=_dingtalk_robot_api.__post__(self,**kwattr)
        if(remsg['errcode']):
            raise DingError('[Error {}]: {}'.format(remsg['errcode'],remsg['errmsg']))

class DingLimit(_dingtalk_robot_within_limit):
    'inherited from _dingtalk_robot_api for sending while you can'
    def __post__(self,**kwattr):
        if(time.time() in self):
            self.__history__[self.robot.webhook] = self.__history__[self.__robot__.webhook][1:] + [ time.time() ]
            return _dingtalk_robot_api.__post__(self,**kwattr)
