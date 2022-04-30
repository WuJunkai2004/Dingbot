# coding=utf-8

import dingbot
import sys

help=u'''钉钉机器人的命令行支持。

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

class config(dingbot._configure_manage):
    __path__ = r'.\dingbot_cli.ini' 
    __inst__ = {u'robot':[]}

    def for_each(self):
        for robot in self.data[u'robot']:
            yield dingbot.DingAPI( dingbot.DingManage(robot) )


bot_config = dingbot.config()
cli_config = config()

class cmd:
    def __init__(self, opt):
        '初始化'
        self.argv = {}      # 内部码
        self.attr = opt     # 外部码
        
        self.option()
        
        handle(self.argv)
    
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
        '将短名转化为可识别的长名'
        keys = list(self.argv.keys())
        maps = {
            '?' : 'help',
            'h' : 'help',
            't' : 'text',
            'i' : 'init',
            's' : 'setup',
            'r' : 'robot',
            'l' : 'list'
        }
        for name in keys:
            if(name in maps.keys()):
                self.argv[ maps[name] ] = self.argv[name]
        
       
class handle:
    __all__ = ['_help','_init','_setup','_robot','_list' ]
    def __init__(self, argv):
        for act in argv.keys():
            if('_{}'.format(act) in self.__all__):
                method = getattr(self,'_{}'.format(act))
                method(argv[act])
                break
                
    def _help(self,para):
        print(help)
    
    def _init(self,para):
        '初始化'
        cli_config.data = {u'robot':None}
        cli_config.save()
        
    def _setup(self,para):
        '登记新的机器人'
        para += [None]
        robot = dingbot.Manage(para[0])
        robot.login(para[1],para[2])
        robot.remember()
        
    def _robot(self,para):
        '登入或登出机器人'
        if  (para[0].lower() == 'login' ):
            cli_config.data[u'robot'] += para[1:]
        elif(para[0].lower() == 'logout' ):
            for item in para[1:]:
                cli_config.data[u'robot'].remove(item)
        else:
            raise RuntimeError
    
    def _list(self,para):
        para += ['all']
        if( para[0] == 'all' ):
            print('\n'.join(bot_config.data.keys()))
        if( para[0] == 'using' ):
            print('\n'.join(cli_config.data[u'robot']))


def install():
    import re
    import os
    comm = os.getcwd() + '\\' + 'CLI.py'
    batc = '@echo off&{} %1 %2 %3 %4 %5 %6 %7 %8 %9'.format(comm)
    path = os.environ.get("PATH").split(";")
    file = None
    for item in path:
        if(re.search('python',item,re.I)):
           file = item + 'dingbot.bat'
           break
    else:
        file = 'C:\\WINDOWS\\system32' + 'dingbot.bat'

    try:
        if(not os.path.exists(file)):
            fin = open(file,'w+')
            fin.write(batc)
            fin.close()
        os.system('cmd')
    except:
        print('Please open with administrator privileges')
        


if(not sys.argv[1:]):
    install()

else:
    c = cmd(sys.argv[1:])
