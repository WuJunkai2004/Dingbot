# Dingbot -- a python object for Dingtalk's robot
##### by WuJunkai ( wujunkai20041123@outlook.com )

### Introduction
　　This is a python object by python 2.7.17,It can run without any other modules.  
　　You even can use it as a command line tool if you import it on python IDLE.
### Usage method
#### import 
　　It won't do anything if you run it directly.So you must use it as a third-party library.  
　　You'd better inport it like this:  
``import share``  
　　Or you can import its underlying layer:  
``from send import *``
　　Then you can use its function easily.  
#### module
　　It's easy to see that it's divided into two modules.The 'send' is the base and the 'share'  
is little higher than 'send'.  
　　the tree for send.py:  
> send.py  
>> urls()  
>> send()  
>> text()  
>> link()  
>> markdown()  
