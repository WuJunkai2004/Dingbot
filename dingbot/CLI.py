# coding=utf-8

import dingbot
import sys

ver = '0.12'
help=u'''钉钉机器人的命令行支持。

dingbot [options...] <content>

options:
  -h  -help     获取帮助
  -i  -init     初始化命令行
  -s  -setup    安装一个钉钉机器人
  -r  -robot    操作已安装的钉钉机器人
  -l  -list     列出指定的机器人
  -t  -text     发送字符串
      -image    发送图片
      -link     发送链接

请使用 dingbot -help <option> 获取详细解释
更多帮助,请访问 https://github.com/WuJunkai2004/Dingbot'''

deta = {
'help':'Usage : dingbot -help <option/all>\n  option  可用的标签\n  all     所有帮助',
'init':"初始化机器人队列, 以便重新开始",
'setup':'',
'robot':'',
'list':'',
'text':'',
'image':'',
'link':''}

class config(dingbot._configure_manage):
    __path__ = r'.\dingbot_cli.ini' 
    __inst__ = {u'robot':[]}

    def __call__(self):
        for robot in self.data[u'robot']:
            yield dingbot.DingAPI( dingbot.Manage(robot) )


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
        '遍历命令, 并转化'
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
            'l' : 'list',
            'v' : 'version'
        }
        for name in keys:
            if(name in maps.keys()):
                self.argv[ maps[name] ] = self.argv[name]
        
       
class handle:
    __all__ = ['_help','_init','_setup','_robot','_list','_version','_text' ]
    def __init__(self, argv):
        for act in argv.keys():
            if('_{}'.format(act) in self.__all__):
                method = getattr(self,'_{}'.format(act))
                method(argv[act])
                break
                
    def _help(self,para):
        if  (len(para)==0):
            print(help)
        elif(len(para)==1 and para[0].lower() in deta.keys()):
                print(deta[para[0]])
        elif(len(para) == 1 and para[0].lower() == 'all'):
            for item in deta:
                print('{} :\n{}\n------'.format(item,deta[item]))
        else:
            print('参数错误')
    
    def _init(self,para):
        '初始化'
        cli_config.data = {u'robot':[]}
        cli_config.save()
        
    def _setup(self,para):
        '登记新的机器人'
        para += [None]
        robot = dingbot.Manage(para[0])
        robot.login('{}={}'.format(para[1],para[2]),para[3])
        robot.remember()
        
    def _robot(self,para):
        '登入或登出机器人'
        if  (para[0].lower() == 'login' ):
            cli_config.data[u'robot'] += para[1:]
        elif(para[0].lower() == 'logout' ):
            for item in para[1:]:
                cli_config.data[u'robot'].remove(item)
        elif(para[0].lower() == 'delete' or para[0].lower() == 'del'):
            for item in para[1:]:
                bot_config.data.pop(item)
        else:
            raise RuntimeError
        bot_config.save()
        cli_config.save()
    
    def _list(self,para):
        para += ['using']
        if( para[0] == 'all' ):
            print('\n'.join(bot_config.data.keys()))
        if( para[0] == 'using' ):
            print('\n'.join(cli_config.data[u'robot']))

    def _version(self,para):
        print('version : ' + ver)

    def _text(self,para):
        for robot in cli_config():
            robot.text(content = para[0])


def install():
    '植入 dingbot'
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
        return os
    except:
        print('Please open with administrator privileges')
        return None
        


if(__name__ == '__main__'):
    if(not sys.argv[1:]):
        success = install()
        if(success):
            print("Dingbot CLI [version {}.0]".format(ver))
            print("Please input \"Dingbot /?\" for more help\n")
            success.system('cmd')

    else:
        c = cmd(sys.argv[1:])
