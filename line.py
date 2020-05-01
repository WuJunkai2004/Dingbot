# coding=utf-8

import manage
import share
import sys
import os

help=u'''钉钉机器人的命令行接口

Dingbot [string]
Dingbot [/N robot] -t text
Dingbot [/N robot] [-u website_url] [-p image_url]
Dingbot [/New new_robot]
Dingbot [/?]|[/H]

  /H /HELP 获取帮助
  /N /NAME 指定发送消息的机器人的名字
     /NEW  新建机器人
  /P /PIC  分享网页图片
  /T /TEXT 发送文本信息
  /U /URL  分享网络连接

    如果对默认的网页分享方式不满意，可以自行定制特殊的展示方法，
也可以到GitHub上汇报，我会尽力提供支持。

更多帮助,请访问 https://github.com/WuJunkai2004/Dingbot'''

cmd=r'''@echo off
echo Dingbot By WuJunkai - 1.00.0
echo more help please view https://github.com/WuJunkai2004/Dingbot
:main
    set "cmd="
    set /P cmd=^>^>^>
    if "%cmd%"=="" goto:main
    for /F "tokens=1*" %%i in ("%cmd%") do if /I "%%i"=="Dingbot" line.py %%j
goto:main'''

attr=sys.argv[1:]
argv={}

if(not attr):
    if(not os.path.exists('.\Dingbot.bat')):
        with open('Dingbot.bat','w') as fout:
            fout.write(cmd)
    os.system('Dingbot.bat')

for i in range(len(attr)):
    if(attr[i][0] in ('/','-')):
        attr[i]=attr[i].lower()
        if  (attr[i][1:] in ('u','url')):
            argv['url']=attr[i+1]
        elif(attr[i][1:] in ('p','pic')):
            argv['pic']=attr[i+1]
        elif(attr[i][1:] in ('t','text')):
            argv['text']=attr[i+1].decode('gbk')
        elif(attr[i][1:] in ('n','name')):
            argv['name']=attr[i+1]
        elif(attr[i][1:] in ('h','help','?')):
            print(help)
            sys.exit()
        elif(attr[i][1:] in ('new')):
            manage.new(attr[i+1])
        else:
            print('WRONG : %s is not a option.'%(attr[i]))
            sys.exit()

if('name' in argv.keys()):
    exec('robot=share.%s'%(argv['name']))
else:
    robot=share.robot

if(len(attr)==1):
    recode=share.share(attr[0].decode('gbk'))

if  ('text' in argv.keys()):
    recode=robot.text(argv['text'])
elif('url' in argv.keys() and 'pic' in argv.keys()):
    recode=robot.push(u'链接','![](%s)'%(argv['pic']),('查看原文',argv['url']))
elif('url' in argv.keys()):
    recode=share.share(argv['url'])
elif('pic' in argv.keys()):
    recode=robot.markdown(u'图片','![](%s)'%(argv['pic']))
print(recode)
