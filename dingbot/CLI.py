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
  -init   -i    初始化命令行的参数，清除载入的机器人
  -setup  -s    安装一个钉钉机器人，用于后续操作
  -robot  -r    载入或者移除机器人，可以同时指定多个。
                当使用发送模块的时候，所有被载入的机器人都会同步发送消息。
  -list   -l    列出所有安装或者载入的机器人，默认为all

dingbot -text content
dingbot -image file-path
dingbot -link url
  钉钉机器人的发送模块
  -text   -t    发送字符串
  -image        发送图片
  -link         发送链接

更多帮助,请访问 https://github.com/WuJunkai2004/Dingbot'''

class config:
    def __init__(self, path=r'.\dingbot_cli.ini'):
        self.path = path
        fin = open(path)
        self.data = json.load(fin)
        fin.close()
    
    def __getattr__(self, name):
        return self.data[name]
    
    def for_each():
        for robot in self.data[u'robot']:
            yield dingbot.DingAPI( dingbot.DingManage(robot) )


bot_config = dingbot._config_manage()
cli_config = config()

class cmd:
    def __init__(self, opt):
        '初始化'
        self.argv = {}      # 内部码
        self.attr = opt     # 外部码
        
        self.option()
        
        self.action()
    
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

    def action(self):
        handle(self.argv)
       
class handle:
    def __init__(self, argv):
        for act in argv.keys():
            if('_{}'.format(act) in self.__all__):
                method = getattr(self,'_{}'.format(act))
                method(argv[act])
                break
                
    def _help(self,para):
        print(help)
    
    def _init(self,para):
        raise None
        
    def _setup(self,para):
        para += [None]
        robot = dingbot.Manage(para[0])
        robot.login(para[1],para[2])
        robot.remember()
        
    def _robot(self,para):
        if  (para[0].lower() == 'login' ):
            raise None
        elif(para[0].lower() == 'logout' ):
            raise None
        else:
            raise RuntimeError
    
    def _list(self,para):
        para += ['all']
