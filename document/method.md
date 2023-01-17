## 使用方法
> 对于部分函数或类的名称，可能有轻微改动使其不适用本文档的演示。  

[管理机器人](#管理群机器人) | [机器人接口](#api的调用方式) |[命令行帮助]() 
--- | --- |--- 
### Step Zero
需要提前在钉钉群内注册一个自定义机器人。并安装`Dingbot`。  
请查看`readme.md`决定哪个模块更适合自己。
```
pip install DingRobotPy
```
或
```
pip install DingBot
```

### DingManage
`DingManage`是`_dingtalk_robot_manage`的接口，提供了非常方便的方法来[管理并调用机器人](#管理群机器人)。   
调用`login()`登记机器人。  
```python
# 导入
import dingbot

# 链接应该为以下格式
webhook='https://oapi.dingtalk.com/robot/send?access_token=XXXXXX'

# 初始化一个机器人并传递webhook
robot=dingbot.DingManage()
robot.login(webhook)

# 发送一条简单的信息
# 请注意，此dome仅演示了最简单的使用方法
revalue=robot.api.text(content=u'我就是我, 是不一样的烟火')

# 检查返回值
print(revalue)
```
推荐使用`加签`选项，可以适应大部分应用场景，并同时保证数据的安全。  
```python
import dingbot

webhook='https://oapi.dingtalk.com/robot/send?access_token=XXXXXX'
secret ='oneoan69fe149fa4849das4dfda1df981d1fa51d8'

robot=dingbot.DingManage()
robot.login(webhook,secret)

revalue=robot.api.text(content=u'我就是我, 是不一样的烟火')
print(revalue)
```
### DingAPI
上面的例子里，发送消息时调用`dingbot.DingManage.api`。  
也可以选择调用`dingbot.DingAPI`达到同样的效果。  
```python
import dingbot

robot = dingbot.DingManage('bluebird')
API = dingbot.DingAPI(robot)

revalue=API.text(content=u'我就是我, 是不一样的烟火')
print(revalue)
```
### DingRaise
发送消息后，无论是否成功，都会得到一个为json类型的返回值。若调用成功，为
```json
{"errcode": 0, "errmsg": "ok"}
```
`dingbot`提供了`DingRaise`的方法来自动检查返回值，并在异常时抛出`dingbot.DingError`。  
通过`dingbot.DingManage.Raise`快速调用本方法。
```python
import dingbot

core = dingbot.DingRaise( dingbot.DingManage( 'bluebird' ) )

try:
    core.text(content=u'我就是我, 是不一样的烟火')
except dingbot.DingError as e:
    print(e)
else:
    print('发送成功')
```
### DingLimit
钉钉机器人消息发送频率限制为每分钟20条。若大量连续发送会被限流10分钟。  
为了防止超出发送频率限制，`Dingbot`提供了`dingbot.DingLimit`来控制发送频率。  
当未超过频率限制时，则正常返回返回值。若即将超过，则停止发送并返回空值。  
通过`dingbot.DingManage.limit`快速调用本方法。
```python
import dingbot,time

core = dingbot.DingLimit( dingbot.DingManage( 'bluebird' ) )

#当返回空值时，延迟1ms再次发送
while(not core.text(content=u'我就是我, 是不一样的烟火') ):
    time.sleep(1)
```
### api的调用方式
钉钉机器人提供了5种不同的信息类型，分别为[text](#text)，[link](#link)，[markdown](#markdown)，[ActionCard](#ActionCard)，[FeedCard](#feedcard)。  
卡片类型的消息可以调用`dict`构建。  
若无特殊说明，字符串的编码均为`UTF-8`。参数对大小写敏感。
#### text
```python
# demo
robot.api.text(content=u'我就是我, 是不一样的烟火')
```
参数 | 类型 | 必选 | 说明
--- | --- | --- | --- 
content | str | √ | 消息内容

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
title | str | √ | 消息标题
text | str | √ | 消息内容。如果太长只会部分展示
messageURL | str | √ | 点击消息跳转的URL
picURL | str | × | 图片URL

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
title | str | √ | 首屏会话透出的展示内容
text | str | √ | markdown格式的消息

目前并不完全支持所有markdown格式，具体支持如下：
<details>
<summary>具体支持的markdown语法</summary>

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

部分html代码，如
<sub>,<small>,<big>
```

</details>

#### ActionCard
ActionCard有两种，分别为[整体跳转ActionCard](#整体跳转actioncard)和[独立跳转ActionCard](#独立跳转actioncard)。  
两种不同的类型共用一个相同的接口，由传入的参数决定具体的消息类型。
##### 整体跳转ActionCard
```python
# demo
robot.api.actionCard(title=u"乔布斯 20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身",
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
title | str | √ | 首屏会话透出的展示内容
text | str | √ | markdown格式的消息
singleTitle | str | √ | 单个按钮的标题。
singleURL | str | √ | 点击singleTitle按钮触发的URL

##### 独立跳转ActionCard
```python
# demo
robot.api.actionCard(title=u"乔布斯 20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身",
                     btnOrientation='0'
                     btns=[
                          dict(title=u"内容不错",
                                       actionURL="https://www.dingtalk.com/"
                                      ),
                          dict(title=u"不感兴趣",
                                       actionURL="https://www.dingtalk.com/"
                                      )
                          ],
                     text=u"""
![screenshot](https://gw.alicdn.com/tfs/TB1ut3xxbsrBKNjSZFpXXcXhFXa-846-786.png) 
### 乔布斯 20 年前想打造的苹果咖啡厅 
Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划
""")
```
参数 | 类型 | 必选 | 说明
--- | --- | --- | ---
title | str | √ | 首屏会话透出的展示内容
text | str | √ | markdown格式的消息
btns | list | √ | 按钮，使用dict构建卡片
btnOrientation | str | × | 0-按钮竖直排列，1-按钮横向排列

dict的参数 | 类型 | 必选 | 说明
--- | --- | --- | ---
title | str | √ | 按钮标题
actionURL | str | √ | 点击按钮触发的URL

#### FeedCard
```python
# demo
robot.api.feedCard(links=[
                        dict(title=u"时代的火车向前开",
                                     messageURL="https://www.dingtalk.com/",
                                     picURL="https://gw.alicdn.com/tfs/TB1ayl9mpYqK1RjSZLeXXbXppXa-170-62.png"
                                    ),
                        dict(title=u"时代的火车向前开2",
                                     messageURL="https://www.dingtalk.com/",
                                     picURL="https://gw.alicdn.com/tfs/TB1ayl9mpYqK1RjSZLeXXbXppXa-170-62.png"
                                    )
                        ])
```
参数 | 类型 | 必选 | 说明
--- | --- | --- | ---
links | list | √ | 链接，使用dict构建卡片

dict的参数 | 类型 | 必选 | 说明
--- | --- | --- | ---
title | str | √ | 单条信息文本
messageURL | str | √ | 点击单条信息到跳转链接
picURL | str | √ | 单条信息后面图片的URL

### 使用@
`dingbot`使用`@`的时需调用 `at()` 方法，指定被@的对象。  
每次发送完信息，`at()`的数据就会重置，需要再次调用 `at()` 方法。  
`dingbot.DingManage.api`由于其特殊的构建方法，不能使用`@`。  
如果在消息里没有指定`@`的位置，会默认加到消息末尾。  
```python
# demo
api=dingbot.DingAPI(robot)
# @的参数使用 at() 传入
api.at(atMobiles=['150XXXXXXXX'],isAtAll=False)

api.text(content=u'我就是我, 是不一样的烟火@150XXXXXXXX')
```
| 参数 | 类型 | 说明 |
| --- | --- | --- |
| atMobiles | list | 手机号为str类型 |
| isAtAll | bool | 是否@所有人 |

### 管理群机器人
为了方便调用不同的机器人，dingbot提供了一种仅需要名字的登陆方法。  
但同时会在本地以明码保存`webhook`和`secret`。
```python
# 保存一个机器人，名字为bluebird（可自行更改）
import dingbot

webhook='https://oapi.dingtalk.com/robot/send?access_token=XXXXXX'
secrec ='oneoan69fe149fa4849das4dfda1df981d1fa51d8'

robot=dingbot.DingManage('bluebird')    # 名称在此处传入
robot.login(webhook,secret)
robot.remember()
```
在用户文件夹下储存着`.dingbot\config.json`的文件，里面保存了`bluebird`的数据。  
`config.json`可存储多个机器人的数据，但需要保证机器人的名字的唯一性。  
如需更改webhook或secret，可以重新调用login()方法，也可以直接对机器人的变量进行赋值。
如以上代码等价于
```python
# 保存一个机器人，名字为bluebird（可自行更改）
import dingbot

robot=dingbot.DingManage('bluebird')
robot.webhook='https://oapi.dingtalk.com/robot/send?access_token=XXXXXX'
robot.secret ='oneoan69fe149fa4849das4dfda1df981d1fa51d8'

robot.remember()
```
如果机器人已经保存，就可以更方便地调用，无论从何处。
```python
# 调用 bluebird
robot=dingbot.DingManage('bluebird')
# 请注意，这里不需要再次调用 login()
robot.api.text(content=u'我就是我, 是不一样的烟火')
```
当然，也可以删除机器人。
```python
robot=dingbot.DingManage('bluebird'）
robot.delete()
```
