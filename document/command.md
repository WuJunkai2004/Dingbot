## 命令行使用方法
命令行仍在不断更新中，因此，本方法内的介绍可能会失效。
请善用`dingbot /h`。
### Step Zero
当安装`Dingbot`(python module)后，即可使用`dingbot`的命令行。  
不过，此时无法通过直接在命令行里面使用`dingbot`。  
需要通过内置的方法，将`dingbot`这一命令，植入系统目录。 
```python
# use python shell
import dingbot.CLI
dingbot.CLI.install()
```
或者，直接双击打开`CLI.py`，将会自动植入并开启命令行。

### 初始化
