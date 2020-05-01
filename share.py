# coding=utf-8

from send import *
from json import dumps as json
from json import loads as jsoff
from re import compile as re

headers={
         'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Mobile Safari/537.36',
         }
try:
    with open('config.json','r') as _fin:
        _config=eval(_fin.read())
except IOError:
    with open('config.json','w') as _fout:
        _fout.write('{}')
    _config={}

if(_config.keys()):
    robot=Dingbot(_config.keys()[0])

def share(url):
    if  (url.find('www.bilibili.com/video')!=-1):
        bilibili_video(url)
    elif(url.find('www.bilibili.com/read')!=-1):
        bilibili_read(url)
    elif(url.find('www.bilibili.com/ranking')!=-1):
        bilibili_rank(url)
    else:
        robot.text(url)

def bilibili_video(url):
    for i in re(r'(?<=<meta ).+?(?=>)').findall(get(seal(url,headers=headers)).read()):
        if  (i.find('itemprop="name"')       !=-1):
            title=re(r'(?<=content=").+(?=")').search(i).group()
        elif(i.find('itemprop="description"')!=-1):
            text =re(r'(?<=content=").+(?=")').search(i).group()
        elif(i.find('itemprop="image"'      )!=-1):
            image=re(r'(?<=content=").+(?=")').search(i).group()
    robot.link(title,text,url,image)

def bilibili_read(url):
    html =get(seal(url,headers=headers)).read()
    title=re(r'(?<=<title>).+?(?=</title>)').search(html).group()
    text =re(r'(?<=<meta name="description" content=").+?(?=">)').search(html).group()
    robot.link(title,text,url,'https://i0.hdslb.com/bfs/archive/4de86ebf90b044bf9ba2becf042a8977062b3f99.png')

def bilibili_rank(url,range=[0,10]):
    html  =get(seal(url,headers=headers)).read()
    lists =jsoff(re(r'(?<=__INITIAL_STATE__=){.+?}(?=;)').search(html).group())['rankList']
    urls  =re(r'(?<=<div class="img"><a href=").+?(?=" target="_blank">)').findall(html)[range[0]:range[1]]
    titles=[]
    images=[]
    for i in lists[range[0]:range[1]]:
        images.append(i['pic'].replace(r'\u002F',r'/'))
        titles.append((i['title']))
    robot.feed(zip(titles,urls,images))

def picture(path=r'D:\用户目录\Pictures\wall.jpg'):
    image=open(path,'rb')
    post()
    pass

def save(url):
    with open('web.txt','w') as fout:
        fout.write(get(seal(url,headers=headers)).read())
