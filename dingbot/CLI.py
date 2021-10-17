# coding=utf-8

import dingbot
import io
import os

import sys

help=u'''钉钉机器人的命令行支持

dingbot -init
dingbot -setup name webhook [secret]
dingbot -robot login/logout name1 [name2...]
dingbot -list [all/using]
  钉钉机器人的管理模块
  -init         初始化机器人的所有参数，清除载入的机器人
  -setup        安装一个钉钉机器人，用于后续操作
  -robot        载入或者移除机器人，可以同时指定多个。
                当使用发送模块的时候，所有被载入的机器人都会同步发送消息。
  -list         列出所有安装或者载入的机器人

dingbot -text content
dingbot -image file-path
dingbot -link url
  钉钉机器人的发送模块
  


更多帮助,请访问 https://github.com/WuJunkai2004/Dingbot'''

attr=sys.argv[1:] #外部命令
argv={}           #内部命令
recode={          #状态码
    'errcode':405,
    'errmsg':'wrong'
    }
                  #读取配置
config = dingbot._configure_manage()

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
            '?' : 'help'
        }
        for name in self.argv.keys():
            if(name in maps.keys()):
                self.argv[ maps[name] ] = self.argv[name]
                
    def load(self):
        pass
                
    def _load_congif(self, path=r'.\dingbot_cli.ini'):
        pass

                  #检查可用与否
if(not argv['name'] and not config.data[u'names'] and not argv['hook']):
    recode['errmsg']='you are not having any dingbot now'
    print(recode)
    sys.exit()

                  #配置机器人
robot = dingbot.DingManage()
if  (not argv['name']):
    if  ('hook' in argv.keys()):
        robot.login(argv['hook'],argv['key'])
    else:
        robot.name = config.data[u'names'][0]
        robot.login()
else:
    if  ('hook' in argv.keys()):
        robot.login(argv['hook'],argv['key'])
        robot.name=argv['name']
        robot.remember()
        recode['errcode']=200
        recode['errmsg'] ='load robot %s successfully'%(argv['name'])
    else:
        robot.name = argv['names']
        robot.login()
        
api = robot.api

if(len(attr)==1): #快捷发送
    recode = api.text(content = attr[0].decode('gbk'))

                  #分析命令
if  ('text' in argv.keys()):
    recode=api.text(content = argv['text'],argv['at'])
elif('url'  in argv.keys() and 'pic' in argv.keys()):
    raise RuntimeError
    recode=robot.card.independent(u'链接','![](%s)'%(argv['pic']),argv['url'])
elif('url'  in argv.keys()):
    raise RuntimeError
    recode=robot.share(argv['url'])
elif('pic'  in argv.keys()):
    recode=robot.markdown(u'图片','![](%s)'%(argv['pic']),argv['at'])
elif('del'  in argv.keys()):
    if(argv['at']==all):
        config.data={"names":[],"robot":[]}
        recode['errcode']=200
        recode['errmsg'] ='delete all of dingbots successfully'
    elif(attr[i+1] in config['names']):
        index=config['names'].index(attr[i+1])
        del config['names'][index]
        del config['robot'][index]
        recode['errcode']=200
        recode['errmsg'] ='delete dingbot %s successfully'%(attr[i+1])
    else:
        recode['errmsg'] ='can not find the robot %s'%(attr[i+1])
    config.save()

print(recode)
