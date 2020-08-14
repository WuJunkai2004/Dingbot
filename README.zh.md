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
　　api的调用格式将在下面给出。
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
### 使用@
　　dingbot 使用`@`的方法与钉钉开发文档内的内容完全相同。使用 at() 指定对象。但是，每次发送完信息，at的数据就会重置，需要再次调用at()方法。  
```python
import dingbot

webhook='https://oapi.dingtalk.com/robot/send?access_token=XXXXXX'
secrec ='oneoan69fe149fa4849das4dfda1df981d1fa51d8'

# 初始化一个机器人并传递webhook和secret
robot=dingbot.DingManage()
robot.login(webhook,secret)

# @的参数使用 at() 传入
robot.at(atMobiles=['150XXXXXXXX'],isAtAll=False)

revalue=robot.api.text(content=u'我就是我, 是不一样的烟火@150XXXXXXXX')
print(revalue)
```
| 参数 | 类型 | 说明 |
| --- | --- | --- |
| atMobiles | list | 手机号必须为str类型 |
| isAtAll | bool | @所有人 |

　　如果在文本里没有指定@的位置，会默认加到末尾。  
　　似乎所有类型的信息都可以使用at()。
