# coding=utf-8
# version=2.10.0

try:
    from urllib2 import urlopen as _urlopen
    from urllib2 import Request as _request

    def _urls(self):
        ## python2 的加密算法
        from urllib import quote_plus as plus
        from base64 import b64encode as base
        from hashlib import sha256 as sha
        from time import time
        from hmac import new
        timestamp          = long(round(time() * 1000))
        secret_enc         = bytes(self._key).encode('utf-8')
        string_to_sign     = '{}\n{}'.format(timestamp, self._key)
        string_to_sign_enc = bytes(string_to_sign).encode('utf-8')
        hmac_code          = new(secret_enc, string_to_sign_enc, digestmod=sha).digest()
        sign               = plus(base(hmac_code))
        return '%s&timestamp=%s&sign=%s'%(self._web,timestamp,sign)

except ImportError:
    from urllib2.request import urlopen as _urlopen
    from urllib2.request import Request as _request

    def _urls(self):
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
        return '%s&timestamp=%s&sign=%s'%(self._web,timestamp,sign)

from re import compile as re
from json import dumps as json
from json import loads as jsoff

get =lambda url,     headers={'User-Agent':'Mozilla/5.0'}       :_urlopen(_request(url,None,headers))
post=lambda url,data,headers={'Content-Type':'application/json'}:_urlopen(_request(url,data,headers))


def configure(file,default={}):
    try:
        fin=open(file,'r')
    except IOError:
        return default
    else:
        config=eval(fin.read())
        fin.close()
        return config

_config=configure('config.json',{"names":[],"robot":[]})


def update():
    old=configure('update.json',{"common":{}})
    up=download('update.json')
    new=eval(up)
    for i in new['common'].keys():
        if(i not in old['common'].keys() or new['common'][i]['date']>old['common'][i]['date']):
            print download(i)
        else:
            print("%s is the newest"%(i))
    fout=open('update.json','w')
    fout.write(up)
    fout.close()


def download(path):
    url='https://github.com/WuJunkai2004/Dingbot/blob/master/%s'%(path)
    try:
        html=get(url).read()
    except:
        return {'errcode':404,'errmsg':'can not connect Github'}
    code=re(r'<td id="LC.+').findall(html)
    code=[''.join(re(r'(?<=>).{0,}?(?=<)').findall(i)) for i in code]
    code='\n'.join(code)
    unes={'&lt;':'<','&nbsp;':' ','&gt;':'>','&quot;':'"','&amp;':'&','&#39;':'\''}
    for i in unes.keys():
        text=re(i).sub(unes[i],code)
    fout=open(path,'w')
    fout.write(code)
    fout.close()
    return {'errcode':200,'errmsg':'update %s successfully'%(path)}


class _info(object):
    ##提取参数
    def __init__(self,webhook,secret=''):
        if(webhook in _config['names']):
            index=_config['names'].index(webhook)
            self._key=_config['robot'][index]['secret']
            self._web=_config['robot'][index]['webhook']
        else:
            self._web=webhook
            self._key=secret
        self._url=lambda:(_urls(self) if(self._key)else self._web)


class _Repeater(_info):
    '中继器'


class Dingbot(_info):
    '钉钉机器人的主体'
    def __init__(self,webhook,secret=''):
        _info.__init__(self,webhook,secret)
        self.card                   =_Repeater(webhook,secret)
        self.card.feed              =self._feed
        self.card.action            =_Repeater(webhook,secret)
        self.card.action.overall    =self._overa
        self.card.action.independent=self._indep

    def save(self,name):
        if(name not in _config['names']):
            _config['names'].append(name)
            _config['robot'].append({'name':name,'secret':self._key,'webhook':self._web})
        else:
            index=_config['names'].index(name)
            _config['robot'][index]['secret'] =self._key
            _config['robot'][index]['webhook']=self._web
        fout=open('config.json','w')
        fout.write(json(_config))
        fout.close()

    def text(self,text,at=[]):
        '文本信息'
        phone=[]
        every=False
        if(at==all):
            every=True
        else:
            phone=list(map(str,at))
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
            phone=list(map(str,at))
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

    def _feed(self,*links):
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

    def _indep(self,title,markdown,url,show=u'阅读全文'):
        msg={
            'msgtype':'actionCard',
            'actionCard':{
                'title':title,
                'text' :markdown,
                'singleTitle'   :show,
                'singleURL'     :url
                }
            }
        return self.send(msg)

    def _overa(self,title,markdown,button):
        if(type(button[0])==str):
            button=[button]
        btns=[{'title':i[0],'actionURL':i[1]} for i in button]
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
        
    def send(self,msg):
        '发送消息'
        recode=post(self._url(),data=json(msg).encode("utf-8"))
        return eval(recode.read())


class DingPlus(Dingbot):
    def share(self,url):
        try:
            html=get(url).read()
        except ValueError:
            return self.text(url)
        try:
            title=re(r'(?<=<title>).+?(?=</title>)').search(html).group()
        except AttributeError:
            return self.markdown(u'图片','![](%s)'%(url))
        print title
