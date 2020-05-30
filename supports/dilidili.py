# coding=utf-8

from dingbot import *
from re import compile as re

headers={
         'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Mobile Safari/537.36',
         }

re_title=re(r'(?<=<title>).+?(?=</title>)')
re_hosts=re(r'.+?[^:^/](?=/)')

class DingPlus(Dingbot):

    def share(self,url):
        if  (url.find('www.bilibili.com/video')!=-1):
            return self.bilibili_video(url)
        elif(url.find('www.bilibili.com/read')!=-1):
            return self.bilibili_read(url)
        elif(url.find('www.bilibili.com/ranking')!=-1):
            return self.bilibili_rank(url)
        else:
            return self.other(url)

    def bilibili_video(self,url):
        html=get(url,headers).read()
        for i in re(r'(?<=<meta ).+?(?=>)').findall(html):
            if  (i.find('itemprop="name"')       !=-1):
                title=re(r'(?<=content=").+(?=")').search(i).group()
            elif(i.find('itemprop="description"')!=-1):
                text =re(r'(?<=content=").+(?=")').search(i).group()
            elif(i.find('itemprop="image"'      )!=-1):
                image=re(r'(?<=content=").+(?=")').search(i).group()
        return self.link(title,text,url,image)

    def bilibili_read(self,url):
        html =get(url,headers).read()
        title=re_title.search(html).group()
        text =re(r'(?<=<meta name="description" content=").+?(?=">)').search(html).group()
        return self.link(title,text,url,'https://i0.hdslb.com/bfs/archive/4de86ebf90b044bf9ba2becf042a8977062b3f99.png')

    def bilibili_rank(self,url,range=[0,10]):
        html  =get(url,headers).read()
        lists =jsoff(re(r'(?<=__INITIAL_STATE__=){.+?}(?=;)').search(html).group())['rankList']
        urls  =re(r'(?<=<div class="img"><a href=").+?(?=" target="_blank">)').findall(html)[range[0]:range[1]]
        titles=[]
        images=[]
        for i in lists[range[0]:range[1]]:
            images.append(i['pic'].replace(r'\u002F',r'/'))
            titles.append((i['title']))
        return self.feed(zip(titles,urls,images))

    def picture(self,path=r'D:\用户目录\Pictures\wall.jpg'):
        image=open(path,'rb')
        post()
        pass

    def other(self,url):
        try:
            html=get(url,headers).read()
        except:
            return self.text(url)
        title=re_title.search(html).group()
        img=re_hosts.search(html).group()+r'/favicon.ico'
        self.link(title,url,img)

def save(url):
    with open('web.txt','w') as fout:
        fout.write(get(url,headers).read())
