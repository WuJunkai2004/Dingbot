# coding=utf-8

try:
    input=raw_input
except ImportError:
    pass

def new(name):
    print(u'请输入机器人的配置')
    webhook=input(u'Webhook:')
    secret =input(u'secret :')
    try:
        with open('config.json','r') as fin:
            config=eval(fin.read())
    except IOError:
        config={}
    config[name]={}
    config[name]['webhook']=webhook
    config[name]['secret' ]=secret
    config=json(config)
    with open('config.json','w') as fout:
        fout.write(config)
    print(u'加载完成')

def table():
    try:
        with open('config.json','r') as fin:
            config=eval(fin.read())
    except IOError:
        config={}
    for i in config.keys():
        print(i)

def json(gets):
    key=gets.keys()
    text='{\n'
    for i in range(len(key)):
        if(i!=0):
            text+='    ,\n'
        text+='    "%s":{\n'%(key[i])
        text+='        "webhook":"%s",\n'%(gets[key[i]]['webhook'])
        text+='        "secret" :"%s"\n'%(gets[key[i]]['secret'])
        text+='    }\n'
    text+='}'
    return text
