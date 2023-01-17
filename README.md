# Dingbot : 一个轻量级的SDK，为钉钉群机器人打造
## 介绍
这是一个轻量级的SDK，依靠[钉钉支持文档](https://open.dingtalk.com/document/group/custom-robot-access)而编写，支持所有机器人的操作。  
本SDK有两个版本，分别为`Dingbot`与`DingRobotPy`。  
| Dingbot | DingRobotPy |
| --- | --- |
| 仅有核心代码 | 附加其他功能，如`命令行`，`提取器` |
| 无需第三方库 | 需前置`requests`库 |
## 安装
```
pip install DingBot
```
或
```
pip install DingRobotPy
```
## 特点
- [x] 超小的代码量，核心代码仅有不到200行  
- [x] 直接调用标准库，无需加装第三方库  
- [x] 可在所有python环境中运行  
- [x] 对官方提供的所有钉钉群机器人接口提供了标准封装  
- [x] 支持命令行操作（持续更新中）
- [x] ~大量的格式支持，可简易地分享网页、图片~  
#### 即将提供的功能
- [ ] 完整的`dingbot.Card`，可对网页、图片、文件进行自动提取内容   
- [ ] 全新的`dingbot.CLI`可在命令行进行大部分操作功能
- [ ] `dingbot.GUI`库，可GUI下完成所有操作*更新中）
## 作者
由 [吴君凯](mailto:wujunkai20041123@outlook.com) 建立框架。  
由 [吴君明](mailto:2706914036@qq.com) 负责漏洞修复与后续支持。
## [使用方法](https://github.com/WuJunkai2004/Dingbot/blob/master/document/method.md)
## [代码原理](https://github.com/WuJunkai2004/Dingbot/blob/master/document/wiki.md)
## 参考
[钉钉支持文档](https://open.dingtalk.com/document/group/custom-robot-access)。
