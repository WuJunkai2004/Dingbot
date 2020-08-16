# Dingbot : 一个为控制钉钉群机器人而生的项目
## 介绍
　　这是一个钉钉机器人 api ，在 python 2.17.7 的环境下编写而成。同时可在 python 3.x 的环境下运行。  
　　除了 python 的内置库，此项目的运行不依赖其他第三方库。  
　　开发者努力让所有人 —— 无论是否接受过编程教育 —— 都可以快速上手，开发了 `line.py` 模块，可用于命令行。  
　　本项目还在快速迭代中，本页的例子可能会失效或超前。此时，请联系 吴君明 进行修改。
## 作者
　　由吴君明 ( 2706914036@qq.com ) 提出编写，并由吴君凯 ( wujunkai20041123@outlook.com ) 最终完成。
## 使用方法
### Step Zero
　　需要提前在钉钉群内注册一个自定义机器人。并下载Dingbot  
```
pip install DingRobotPy
```
### 开始使用
　　`webhook`是必须的，因为这是接口的链接。  
```python
# 导入
import dingbot

# 链接应该为以下格式
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
　　但是上述用法是不推荐的。这里推荐安全设置使用 加签。加签可以适应大部分应用场景，同时保证机器人的安全性。  
　　dingbot默认机器人的安全设置为加签。
```python
import dingbot

webhook='https://oapi.dingtalk.com/robot/send?access_token=XXXXXX'
secret ='oneoan69fe149fa4849das4dfda1df981d1fa51d8'

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

#### markdown
```python
# demo
robot.api.markdown(title=u"杭州天气",
                   text=u"""
#### 杭州天气
> 9度，西北风1级，空气良89，相对温度73%
> ![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)
> ###### 10点20分发布 [天气](https://www.dingtalk.com) 
""")
```
参数 | 类型 | 必选 | 说明
--- | --- | --- | ---
title | str | YES | 首屏会话透出的展示内容
text | str | YES | markdown格式的消息

　　目前并不完全支持所有markdown格式，具体支持如下：
```
文本
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题

引用
> A man who stands for nothing will fall for anything.

文字加粗、斜体
**bold**
*italic*

链接、图片
[this is a link](http://name.com)
![](http://name.com/pic.jpg)

无序列表
- item1
- item2

有序列表
1. item1
2. item2
```

#### ActionCard
　　ActionCard分为两种，分别为整体跳转ActionCard类型和独立跳转ActionCard类型。  
　　两种不同的类型共用一个相同的接口，由传入的参数决定具体的消息类型。
##### 整体跳转ActionCard
```python
# demo
robot.api.ActionCard(title=u"乔布斯 20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身",
                     singleURL="https://www.dingtalk.com/",
                     singleTitle=u'阅读全文',
                     text=u"""
![screenshot](https://gw.alicdn.com/tfs/TB1ut3xxbsrBKNjSZFpXXcXhFXa-846-786.png) 
### 乔布斯 20 年前想打造的苹果咖啡厅 
Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划
""")
```
参数 | 类型 | 必选 | 说明
--- | --- | --- | ---
title | str | YES | 首屏会话透出的展示内容
text | str | YES | markdown格式的消息
singleTitle | str | YES | 单个按钮的标题。
singleURL | str | YES | 点击singleTitle按钮触发的URL

##### 独立跳转ActionCard
```python
# demo
robot.api.ActionCard(title=u"乔布斯 20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身",
                     btnOrientation='0'
                     btns=[
                          dingbot.Card(title=u"内容不错",actionURL="https://www.dingtalk.com/"),
                          dingbot.Card(title=u"不感兴趣",actionURL="https://www.dingtalk.com/")
                          ],
                     text=u"""
![screenshot](https://gw.alicdn.com/tfs/TB1ut3xxbsrBKNjSZFpXXcXhFXa-846-786.png) 
### 乔布斯 20 年前想打造的苹果咖啡厅 
Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划
""")
```
参数 | 类型 | 必选 | 说明
--- | --- | --- | ---
title | str | YES | 首屏会话透出的展示内容
text | str | YES | markdown格式的消息
btns | list | YES | 按钮，为dingbot.Card或dict类型
btnOrientation | str | NO | 0-按钮竖直排列，1-按钮横向排列

dingbot.Card的参数 | 类型 | 必选 | 说明
--- | --- | --- | ---
title | str | YES | 按钮标题
actionURL | str | YES | 点击按钮触发的URL

#### FeedCard
```python
# demo
robot.api.FeedCard(links=[
                        dingbot.Card(title=u"时代的火车向前开",messageURL="https://www.dingtalk.com/",picURL="https://gw.alicdn.com/tfs/TB1ayl9mpYqK1RjSZLeXXbXppXa-170-62.png",
                        dingbot.Card(title=u"时代的火车向前开2",messageURL="https://www.dingtalk.com/",picURL="https://gw.alicdn.com/tfs/TB1ayl9mpYqK1RjSZLeXXbXppXa-170-62.png"
                        ])
```
参数 | 类型 | 必选 | 说明
--- | --- | --- | ---
links | list | YES | 链接，为dingbot.Card或dict类型

dingbot.Card的参数 | 类型 | 必选 | 说明
--- | --- | --- | ---
title | str | YES | 单条信息文本
messageURL | str | YES | 点击单条信息到跳转链接
picURL | str | YES | 单条信息后面图片的URL

### 使用@
　　dingbot 使用`@`的方法与钉钉开发文档内的内容完全相同。调用 `at()` 方法，指定被@的对象。  
　　每次发送完信息， `at()` 的数据就会重置，需要再次调用 `at()` 方法。  
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
　　`config.json`可存储同时多个机器人的数据，但需要保证机器人的名字各不相同。  
　　如需更改webhook或secret，可以重新调用login()方法，也可以直接对机器人的变量进行赋值。
```python
# 调用 bluebird
robot=dingbot.DingManage('bluebird')

robot.api.text(content=u'我就是我, 是不一样的烟火')
```
　　当然，也可以删除机器人。
```pyhton
robot=dingbot.DingManage('bluebird'）
robot.delete()
```
## 参考
https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq
