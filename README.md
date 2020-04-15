# Dingbot -- a python object for Dingtalk's robot
##### by WuJunkai ( wujunkai20041123@outlook.com )

### Introduction
　　This is a python object by python 2.7.17,It can run without any other modules.  
　　You even can use it as a command line tool if you import it on python IDLE.
### Usage method
#### module
　　It's easy to see that it's divided into two modules.The `send.py` is the base and the `share.py`  
is little higher than `send.py`.  
　　The tree for `send.py`:  
> send.py  
>> urls()  
>> send()  
>> text()  
>> link()  
>> markdown()  
>> push()  
>> feed()  

　　`send.py` is the base of the library.So unless there is a bug, it will not be updated.  
　　`share.py` encapsulates the sharing links of some common websites.It may be updated frequently.
#### prepare
　　First,you should have the Webhook and the key for a Dingtalk robot.And its security settings  
should be signed.  
　　Then build `config.json` newly.You should save data of the Dingtalk robot in the following format.  
```
[
    Wekhook,
    key
]
```
#### import 
　　It won't do anything if you run it directly.So you must use it as a third-party library.  
　　You'd better inport it like this:  
``import share``  
　　Or you can import its underlying layer:  
``from send import *``  
　　Then you can use its function easily.  
#### use
　　If you import `share.py`,you can 