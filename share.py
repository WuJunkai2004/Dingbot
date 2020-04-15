# coding=utf-8

from send import *
from re import compile as re

headers={
         'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Mobile Safari/537.36',
         }

def share(url):
    if(url.find('www.bilibili.com/video')!=-1):
        bilibili_video(url)
    else:
        raise RuntimeError('Can not supprt the url')

def weibo(url):
    link(u'微博',u'随时随地发现新鲜事！微博带你欣赏世界上每一个精彩瞬间，了解每一个幕后故事。分享你想表达的，让全世界都能听到你的心声！',url,'http://www.sinaimg.cn/blog/developer/wiki/LOGO_64x64.png')

def bilibili_video(url):
    for i in re(r'(?<=<meta ).+?(?=>)').findall(get(seal(url,headers=headers)).read()):
        if  (i.find('itemprop="name"')       !=-1):
            title=re(r'(?<=content=").+(?=")').search(i).group()
        elif(i.find('itemprop="description"')!=-1):
            text =re(r'(?<=content=").+(?=")').search(i).group()
        elif(i.find('itemprop="image"'      )!=-1):
            image=re(r'(?<=content=").+(?=")').search(i).group()
    link(title,text,url,image)

def bilibili_read(url):
    html =get(seal(url,headers=headers)).read()
    title=re(r'(?<=<title>).+?(?=</title>)').search(html).group()
    text =re(r'(?<=<meta name="description" content=").+?(?=">)').search(html).group()
    link(title,text,url,'https://i0.hdslb.com/bfs/archive/4de86ebf90b044bf9ba2becf042a8977062b3f99.png')

def save(url):
    with open('web.txt','w') as fout:
        fout.write(get(seal(url,headers=headers)).read())
