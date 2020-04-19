# Dingbot -- a python object for Dingtalk's robot
##### By Wu Junkai ( wujunkai20041123@outlook.com )
##### And Wu Junming ( 2706914036@qq.com )

### Introduction
　　This is a python object by python 2.7.17,It can run without any other modules.  
　　You even can use it as a command line tool if you import it on python IDLE or run `line.py`.
### Usage method
#### module
　　Now,The library divided into three modules.The `send.py` is the base and the `share.py`  
is little higher than `send.py`.  
　　The tree for `send.py`:  
> send.py  
>> def \_python2()  
>> def \_python2()  
>> class Dingbot()  
>>> def \_\_init\_\_(name)  
>>> def send(msg)  
>>> def text(text,at=\[\])  
>>> def link(title,text,url,pic='')  
>>> def markdown(title,markdown,ar=\[\])  
>>> def push(title,markdown,\*button)  
>>> def feed(\*link)  

　　`send.py` is the base of the library.So unless there is a bug, it will not be updated.  
　　`share.py` encapsulates the sharing links of some common websites.It may be updated frequently.
#### prepare
　　First,you should have the Webhook and the key for a Dingtalk robot.And its security settings  
should be signed.  
　　Then build `config.json` newly.You should save data of the Dingtalk robot in the following format.  
```json  
{
    "robot1":{
        "webhook":"https://oapi.dingtalk.com/robot/send?accxxxxxx",
        "secret" :"SEC06ad3d373xxxxxx"
    },
    "robot2":{
        "webhook":"https://oapi.dingtalk.com/robot/send?ssssss",
        "secret" :"sssssssssss"
    }
}
```
#### import 
　　It won't do anything if you run it directly.So you must use it as a third-party library.  
　　You'd better inport it like this:  
```python  
import share
```  
　　Or you can import its underlying layer:  
```python  
from send import *
``` 
　　Then you can use its function easily.  
#### use
　　If you import `share.py`,you can 
