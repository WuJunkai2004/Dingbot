# Dingbot底层实现原理
## 关于
　　`dingbot`实现了大部分的钉钉机器人的接口，同时提供了表层方法调用底层。  
　　但是，如果有人想要更进一步使用的话，表层方法肯定是不够的。  
　　因此，本文档着重解释`dingbot`中的底层算法，涉及到表层的会一笔带过。  
## 表层接口
　　仅需了解表层接口涉及到哪些底层算法，其他的不重要。

名称 | 类型 | 继承至
--- | --- | ---
Card | function |
DingManage | class | \_dingtalk\_robot\_manage
Dingapi | class | \_dingtalk\_robot\_api
Dingraise | class | \_dingtalk\_robot\_api

## 底层接口
### 目录
名称 | 类型 | 继承至
--- | --- | --- 
\_http\_manage | function | 
\_http\_get | function | \_http\_manage
\_http\_post | function | \_http\_manage
\_configure\_manage | class |
\_dingtalk\_robot\_api | class |
\_dingtalk\_robot\_signature | class | 
\_dingtalk\_robot\_manage | class | \_dingtalk\_robot\_signature

### \_http\_manage
　　`_http_manage`是`dingbot`的网络访问接口，是对`urlopen`的简单封装，提供了非常基础的功能。  
　　传入`url`，`data`，`headers`,返回得到的网页内容。
### \_http\_get
　　继承至`_http_manage`，简化了传入数据。  
　　传入`url`，`headers`返回得到的网页。
### \_http\_post
　　用法与`_http_manage`相同。
### \_configure\_manage
　　用于处理保存在本地的机器人数据。初始化时，可以传入所保存数据的路径，或默认选择本级文件夹内的`config.json`。  
　　一般情况下不会调用到本方法。  
　　`_dingtalk_robot_manage`中的`conf`调用本接口实现，因此可以采用以下方法加载一个特定文件内的机器人数据。  
```python
robot=dingbot.DingManage('blue')

robot.conf.path=r'D:\blue\blue.json'
robot.conf.load()  # 需要重新加载数据

robot.login()      # 需要重新登录
```
　　内置变量说明  
名称 | 类型 | 说明
--- | --- | ---
data | dist | 文件数据
path | str | 文件的保存路径
load | function | 将文件载入`data`
save | function | 将数据保存进文件里

### \_dingtalk\_robot\_api
　　这是`dingbot`的核心，提供了钉钉机器人所有消息类型的接口。`dingapi`、`dingraise`和`dinglimit`直接由此继承。  
　　但实际上，`dingtalk_robot_api`仅仅提供了一个接口`__post__`，所有的消息其实都是调用`__post__`发送。  
　　内置变量说明  
名称 | 类型 | 说明
--- | --- | ---
\_\_robot\_\_ | Dingbot.DingManage | 需要机器人的发送链接
\_\_api\_\_ | str | 本次消息的发送类型
\_\_at\_\_ | dist | @的数据
\_\_getattr\_\_ | function | 设置`__api__`
\_\_dir\_\_ | function | 虚构消息接口
\_\_post\_\_ | function | 发送消息
at | function | 设置`__at__`

　　在调用一个消息接口时，`__getattr__`会取得该消息的类型,储存于`__api__`，并返回`__post__`。  
　　`__post__`需要传入带参数名的不定长参数，并结合其他数据打包形成标准的待发送数据，并发送，返回解析过的返回值。  
因此
```python
api = dingbot.Dingapi( robot )
api.text(content=u'我在测试')
```
等同于
```python
api = dingbot.Dingapi( robot )
api.__api__ = 'text'
api.__post__(content=u'我在测试')
```
