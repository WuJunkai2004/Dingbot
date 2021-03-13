# coding=utf-8

import dingbot
import io
import os

import sys

help=u'''钉钉机器人的命令行程序
! 本程序已过时，将在 dingbot.Card 完成后重写

dingbot [string]
dingbot -del [robot|/a]
dingbot -help
dingbot -list
dingbot [-n robot]
dingbot [-n robot] -hook webhook [-key secret]
dingbot [-n robot] -url urls
dingbot [-n robot] -pic pics

发送模式:
  /N /NAME 指定所操作的机器人
  /P /PIC  分享图片
  /T /TEXT 发送文本，可与/PIC连用
  /U /URL  分享链接，可与/PIC连用

管理模式:
  /A /ALL  @所有人或删除所有机器人，仅可与/TEXT或/DEL连用
  /D /DEL  删除机器人
  /H /HELP 获取帮助
     /HOOK 构建机器人，可指定名称和密钥。若指定名称，则保存此机器人的设置
  /K /KEY  指定密钥
  /L /LIST 机器人名单

更多帮助,请访问 https://github.com/WuJunkai2004/Dingbot'''

cmd=r'''@echo off
echo Dingbot By WuJunkai - 2.00.0
echo more help please view https://github.com/WuJunkai2004/Dingbot
:main
    set "cmd="
    set /P cmd=^>^>^>
    if "%cmd%"=="" goto:main
    if /I "%cmd:~0,7%"=="Dingbot" (line.py%cmd:~7%) else (%cmd%)
goto:main'''

attr=sys.argv[1:] #外部命令
argv={            #内部命令
    'name':'',
    'at':[]
    }
recode={          #状态码
    'errcode':405,
    'errmsg':'wrong'
    }

if(not attr):     #若直接启动
    if( not io.path.isfile('Dingbot.bat') ):
        fout=open('Dingbot.bat','w')
        fout.write(cmd)
        fout.close()
    os.system('Dingbot.bat')
    sys.exit()
                  #读取配置
config = dingbot._configure_manage()

                  #遍历命令
for i in range(len(attr)):
    if(attr[i][0] in (r'/','-')):
        code=attr[i].lower()[1:]
        if  (code in ('a','all')):      #@all
            argv['at']=all
        elif(code in ('d','del')):      #删除机器人
            argv['del']=attr[i+1]
        elif(code in ('h','help','?')): #帮助
            print(help)
            sys.exit()
        elif(code ==      'hook'):      #配置机器人
            argv['hook']=attr[i+1]
            if('key' not in argv.keys()):
                argv['key']=''
        elif(code in ('k','key')):       #获取密匙
            argv['key']=attr[i+1]
        elif(code in ('l','list')):     #列表机器人
            print('\n'.join(config.data[u'names']))
            sys.exit()
        elif(code in ('n','name')):     #指定名称
            argv['name']=attr[i+1]
        elif(code in ('p','pic')):      #发送带图片的消息
            argv['pic']=attr[i+1]
        elif(code in ('t','text')):     #发送文本消息
            argv['text']=attr[i+1]
        elif(code in ('u','url')):      #发送链接
            argv['url']=attr[i+1]
        else:
            recode['errmsg']='%s is not an option'%(code)

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
