# Dingbot底层实现原理
## 关于
　　`dingbot`实现了大部分的钉钉机器人接口，同时提供了相应的表层方法，使其调用底层。  
　　本文档着重解释`dingbot`中的底层算法。  
## 表层接口
名称 | 类型 | 继承至
--- | --- | ---
Card | function |
DingAPI | class | \_dingtalk\_robot\_api
DingError | class | \_\_builtins\_\_.RuntimeError
DingLimit | class | \_dingtalk\_robot\_api
DingManage | class | \_dingtalk\_robot\_manage
DingRaise | class | \_dingtalk\_robot\_api

## 底层接口
### 目录
名称 | 类型 
--- | ---
\_http\_manage | function  
\_http\_get | function  
\_http\_post | function 
\_signature | function 
\_configure\_manage | class 
\_dingtalk\_robot\_api | class 
\_dingtalk\_robot\_manage | class 

### \_http\_manage
　　`_http_manage`是`dingbot`的基础网络访问接口，是对`urlopen`的简单封装。  
　　传入 `url`，`data`，`headers`。  
　　返回 得到的网页内容。
### \_http\_get
　　调用`_http_manage`，简化了传入数据。  
　　传入 `url`，`headers`。  
　　返回 得到的网页。
### \_http\_post
　　用法与`_http_manage`相同。
### \_configure\_manage
　　用于处理保存在本地的机器人数据。  
　　初始化时，可以传入所保存数据的路径，或默认选择`.\config.json`。  
　　`_dingtalk_robot_manage`中的`conf`调用本接口实现，可以采用以下方法加载一个特定文件内的机器人数据。  
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
　　提供了钉钉机器人所有消息类型的接口。  
　　`dingAPI`直接继承此类。其他接口继承后有部分重写。  
　　实际上，`dingtalk_robot_api`仅仅提供了一个接口函数`send`，所有的消息都调用该函数发送。  
　　内置变量说明  

名称 | 类型 | 说明
--- | --- | ---
\_\_robot\_\_ | Dingbot.DingManage | 需要机器人的发送链接
\_\_api\_\_ | str | 本次消息的发送类型
\_\_at\_\_ | dist | @的数据
\_\_getattr\_\_ | function | 设置`__api__`，及接口类型
at | function | 设置`__at__`
send | function | 构建json，发送消息

　　在调用任何一个消息接口时，`__getattr__`会取得该接口的名称的字符串,储存于`__api__`，并返回`send`。  
　　`send`需要传入带参数名的不定长参数，并结合其他数据打包形成标准的`json`格式并发送，同时返回解析过的返回值。  
因此
```python
api = dingbot.DingAPI( robot )
api.text(content=u'我在测试')
```
等同于
```python
api = dingbot.DingAPI( robot )
api.__api__ = 'text'
api.send(content=u'我在测试')
```
