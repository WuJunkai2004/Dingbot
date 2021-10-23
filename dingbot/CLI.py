# coding=utf-8

import dingbot
import io
import json

import os
import sys

help=u'''钉钉机器人的命令行支持

dingbot -init
dingbot -setup name webhook [secret]
dingbot -robot login/logout name1 [name2...]
dingbot -list [all/using]
  钉钉机器人的管理模块
  -init   -i    初始化机器人的所有参数，清除载入的机器人
  -setup  -s    安装一个钉钉机器人，用于后续操作
  -robot  -r    载入或者移除机器人，可以同时指定多个。
                当使用发送模块的时候，所有被载入的机器人都会同步发送消息。
  -list   -l    列出所有安装或者载入的机器人

dingbot -text content
dingbot -image file-path
dingbot -link url
  钉钉机器人的发送模块
  -text   -t    发送字符串
  -image        发送图片
  -link         发送链接

更多帮助,请访问 https://github.com/WuJunkai2004/Dingbot'''

attr=sys.argv[1:] #外部命令
argv={}           #内部命令
recode={          #状态码
    'errcode':405,
    'errmsg':'wrong'
    }
                  #读取配置
config = dingbot._configure_manage()

class config:
    def __init__(self, path=r'.\dingbot_cli.ini'):
        self.path = path
        fin = open(path)
        self.data = json.load(fin)
        fin.close()
    
    def __getattr__(self, name):
        return self.data[name]

class cmd:
    def __init__(self, opt):
        '初始化'
        self.argv = {}
        self.attr = opt
        
        self.robots = []
        
        self.option()
        self.load()
    
    def option(self):
        '遍历命令，并转化'
        for item in self.attr:
            if(item[0] in r'\/-'):
                sets = item[1:]
                self.argv[ sets.lower() ] = []
            else:
                self.argv[ sets.lower() ].append( item )
        self._synonym_option()
    
    def _synonym_option(self):
        maps = {
        #   短名：长名
            '?' : 'help',
            't' : 'text',
            'i' : 'init',
            's' : 'setup',
            'r' : 'robot',
            'l' : 'list'
        }
        for name in self.argv.keys():
            if(name in maps.keys()):
                self.argv[ maps[name] ] = self.argv[name]
                
    def load(self):
        con = config(r'.\dingbot_cli.ini')
        self.robots = con.robot

    def form(self):
        if({'text','image','link'}&set(self.argv.keys())):
            return self._p
        else:
            return self._m
    
    def _p(self):
        if  ('text'  in self.argv.keys()):
            post_module(self.robots,'text',content=argv['text'][0])
        elif:
            raise RuntimeError
