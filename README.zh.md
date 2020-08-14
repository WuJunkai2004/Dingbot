# Dingbot  :  一个为控制钉钉群机器人而生的项目
## 介绍
　　这是一个钉钉机器人 api ，在 python 2.17.7 的环境下编写而成。同时可在 python 3.x 的环境下运行。  
　　除了 python 的内置库，此项目的运行不依赖其他第三方库。  
　　开发者努力让所有人 —— 无论是否接受过编程教育 —— 都可以快速上手，开发了 `line.py` 模块，可用于命令行。
## 作者
　　由吴君明 ( 2706914036@qq.com ) 提出编写，并由吴君凯 ( wujunkai20041123@outlook.com ) 最终完成。
## 使用方法
### Step Zero
　　需要提前在钉钉群内注册一个自定义机器人。并下载Dingbot  
```
pip install dingrobotpy
```
### 开始使用
　　`webhook`是必须的，因为这是接口的链接。  
```python
# 导入
import dingbot

# 链接应该为这个格式
webhook='https://oapi.dingtalk.com/robot/send?access_token=XXXXXX'

# 初始化一个机器人并传递webhook
robot=dingbot.DingManage()
robot.login(webhook)

# 声明安全设置为 非加签
robot.signature=False

# 发送一条简单的信息
revalue=robot.api.text(content=u'我就是我, 是不一样的烟火')

# 检查返回值
print(revalue)
```
　　但是上述写法是不推荐的。这里还是推荐安全设置使用 加签。加签可以适应大部分应用场景，同时保证机器人的安全性。  
　　dingbot默认机器人的安全设置为加签。
```python
import dingbot

webhook='https://oapi.dingtalk.com/robot/send?access_token=XXXXXX'
secrec ='oneoan69fe149fa4849das4dfda1df981d1fa51d8'

# 初始化一个机器人并传递webhook和secret
robot=dingbot.DingManage()
robot.login(webhook,secret)

revalue=robot.api.text(content=u'我就是我, 是不一样的烟火')
print(revalue)
```
### api的调用方式
　　钉钉机器人提供了5种不同的信息类型，分别为text,link,markdown,ActionCard,FeedCard。  
　　若无特殊说明，字符串的编码均为 UTF-8 。参数对大小写敏感。
#### text
```python
# demo
robot.api.text(content=u'我就是我, 是不一样的烟火')
```
参数 | 类型 | 必选 | 说明
--- | --- | --- | --- 
content | str | YES | 消息内容

#### link
```python
# demo
robot.api.link(text=u"这个即将发布的新版本，创始人xx称它为红树林。而在此之前，每当面临重大升级，产品经理们都会取一个应景的代号，这一次，为什么是红树林",
               title=u"时代的火车向前开",
               messageUrl="https://www.dingtalk.com/",
               picUrl='https://gw.alicdn.com/tfs/TB1aNrLGlr0gK0jSZFnXXbRRXXa-202-76.png')
```
参数 | 类型 | 必选 | 说明
--- | --- | --- | ---
title | str | YES | 消息标题
text | str | YES | 消息内容。如果太长只会部分展示
messageURL | str | YES | 点击消息跳转的URL
picURL | str | NO | 图片URL

### 使用@
　　dingbot 使用`@`的方法与钉钉开发文档内的内容完全相同。调用 at() 方法，指定被@指定对象。  
　　每次发送完信息，at的数据就会重置，需要再次调用at()方法。  
　　如果在消息里没有指定@的位置，会默认加到消息末尾。  
```python
# demo

# @的参数使用 at() 传入
robot.at(atMobiles=['150XXXXXXXX'],isAtAll=False)

robot.api.text(content=u'我就是我, 是不一样的烟火@150XXXXXXXX')
```
| 参数 | 类型 | 说明 |
| --- | --- | --- |
| atMobiles | list | 手机号必须为str类型 |
| isAtAll | bool | 是否@所有人 |

### 管理群机器人
　　为了方便调用不同的机器人，dingbot提供了一种仅需要名字的使用方法。但同时会在本地以明码保存webhook和secret。
```python
'''
保存一个机器人，名字为bluebird（可自行更改）
'''
import dingbot

webhook='https://oapi.dingtalk.com/robot/send?access_token=XXXXXX'
secrec ='oneoan69fe149fa4849das4dfda1df981d1fa51d8'


robot=dingbot.DingManage('bluebird')    # 名称在此处传入
robot.login(webhook,secret)
robot.remember()
```
　　现在，你应该可以在本地发现一个`config.json`的文件，里面储存了 bluebird 的数据。
```python
'''
调用bluebird
'''
import dingbot

robot=dingbot.DingManage('bluebird')

robot.api.text(content=u'我就是我, 是不一样的烟火')
```
　　当然，也可以删除机器人。
```pyhton
'''
删除bluebird
'''
import dingbot

robot=dingbot.DingManage('bluebird'）
robor.delete()
```
