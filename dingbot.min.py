try:
    from urllib2 import urlopen as _urlopen
    from urllib2 import Request as _request
except ImportError:
    from urllib.request import urlopen as _urlopen
    from urllib.request import Request as _request
else:python=2
from re import compile as re
from json import dumps as json
from json import loads as jsoff
get =lambda url,     headers={'User-Agent':'Mozilla/5.0'}       :_urlopen(_request(url,None,headers))
post=lambda url,data,headers={'Content-Type':'application/json'}:_urlopen(_request(url,data,headers))
def GET_URL():
    from base64  import b64encode as base
    from hashlib import sha256 as sha
    from time import time
    from hmac import new
    def python2(s):
        from urllib import quote_plus as plus
        timestamp          = long(round(time() * 1000))
        secret_enc         = bytes(s._key).encode('utf-8')
        string_to_sign     = '{}\n{}'.format(timestamp, s._key)
        string_to_sign_enc = bytes(string_to_sign).encode('utf-8')
        hmac_code          = new(secret_enc, string_to_sign_enc, digestmod=sha).digest()
        sign               = plus(base(hmac_code))
        return '%s&timestamp=%s&sign=%s'%(s._web,timestamp,sign)
    def python3(s):
        from urllib.parse import quote_plus as plus
        timestamp          = str(round(time.time() * 1000))
        secret_enc         = secret.encode('utf-8')
        string_to_sign     = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code          = new(secret_enc, string_to_sign_enc, digestmod=sha).digest()
        sign               = plus(base64.b64encode(hmac_code))
        return '%s&timestamp=%s&sign=%s'%(s._web,timestamp,sign)
    return python2 if(python==2)else python3
def configure(file,default={}):
    try:fin=open(file,'r')
    except IOError:return default
    else:
        config=eval(fin.read())
        fin.close()
        return config
_config=configure('config.json',{"names":[],"robot":[]})
class _info(object):
    def __init__(s,webhook,secret=''):
        if(webhook in _config['names']):
            index=_config['names'].index(webhook)
            s._key=_config['robot'][index]['secret']
            s._web=_config['robot'][index]['webhook']
        else:
            s._web=webhook
            s._key=secret
        s._url=lambda:(GET_URL()(s) if(s._key)else s._web)
class _R(_info):
    pass
class Dingbot(_info):
    def __init__(s,webhook,secret=''):
        _info.__init__(s,webhook,secret)
        s.card                   =_R(webhook,secret)
        s.card.feed              =s._feed
        s.card.action            =_R(webhook,secret)
        s.card.action.overall    =s._overa
        s.card.action.independent=s._indep
    def save(s,name):
        if(name not in _config['names']):
            _config['names'].append(name)
            _config['robot'].append({'name':name,'secret':s._key,'webhook':s._web})
        else:
            index=_config['names'].index(name)
            _config['robot'][index]['secret'] =s._key
            _config['robot'][index]['webhook']=s._web
        fout=open('config.json','w')
        fout.write(json(_config))
        fout.close()
    def text(s,text,at=[]):
        phone=[]
        every=0
        if(at==all):every=1
        else:phone=list(map(str,at))
        msg={'msgtype':'text','text':{"content":text},'at':{'atMobiles':phone,'isAtAll':every}}
        return s.send(msg)
    def link(s,title,text,url,pic=''):
        msg={'msgtype':"link",'link':{'title':title,'text':text,'messageUrl':url,'picUrl':pic}}
        return s.send(msg)
    def markdown(s,title,markdown,at=[]):
        phone=[]
        every=0
        if(at==all):every=1
        else:phone=list(map(str,at))
        msg={"msgtype":"markdown","markdown":{"title":title,"text":markdown},'at':{'atMobiles':phone,'isAtAll':every}}
        return s.send(msg)
    def _feed(s,*links):
        if(len(links)==1 and type(links[0])!=str):links=links[0]
        link=list(map(dict,map(lambda x:zip(('title','messageURL','picURL'),x),links)))
        msg={"msgtype":"feedCard","feedCard":{'links':link}}
        return s.send(msg)
    def _indep(s,title,markdown,url,show=u'阅读全文'):
        msg={'msgtype':'actionCard','actionCard':{'title':title,'text':markdown,'singleTitle':show,'singleURL':url}}
        return s.send(msg)
    def _overa(s,title,markdown,button):
        if(type(button[0])==str):button=[button]
        btns=[{'title':i[0],'actionURL':i[1]} for i in button]
        msg={"msgtype": "actionCard","actionCard":{"title":title,"text":markdown,"btns" : btns,'btnOrientation':'0',}}
        return s.send(msg)
    def send(s,msg):
        recode=post(s._url(),json(msg).encode("utf-8"))
        return eval(recode.read())
class DingPlus(Dingbot):
    head={'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N; Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'}
    def share(s,url):
        try:html=get(url,s.head).read()
        except ValueError:return s.text(url)
        try:title=re(r'(?<=>).[^>]+?(?=</title>)').search(html).group()
        except AttributeError:return s.markdown(u'图片','![](%s)'%(url))
        img=re(r'(?<=").[^"]+?(jpg|jpeg|png)(@.+\.webp)?(?=")').search(html)
        img=img.group().split('@')[0] if(img)else ''
        if(img[:2]=='//'):img='http:'+img
        text=re(r'(?<=>).[^>]+?(?=(</p>|</h[1-6]>|</strong>))').search(html)
        text=text.group() if(text)else u'查看全文'
        return s.link(title,text,url,img)
