# coding=utf-8

from send import *
from re import compile as re

headers={
         'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Mobile Safari/537.36',
         }

def share(url):
    if(url.find('www.bilibili.com/video')!=-1):
        video(url)
    else:
        raise RuntimeError('Can not supprt the url')

def weibo(url):
    pass

def video(url):
    for i in re(r'(?<=<meta ).+?(?=/>)').findall(get(seal(url,headers=headers)).read()):
        if  (i.find('itemprop="name"')       !=-1):
            title=re(r'(?<=content=").+(?=")').search(i).group()
        elif(i.find('itemprop="description"')!=-1):
            text =re(r'(?<=content=").+(?=")').search(i).group()
        elif(i.find('itemprop="image"'      )!=-1):
            image=re(r'(?<=content=").+(?=")').search(i).group()
    link(title,text,url,image)

def save(url):
    with open('web.txt','w') as fout:
        fout.write(get(seal(url,headers=headers)).read())
