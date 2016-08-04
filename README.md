#program_wrapper<br/>
#INSTALL
```bash
git clone https://www.github.com/ShichaoMa/program_wrapper.git
```
#HELLOWORLD
##demo1
```python
# -*- coding:utf-8 -*-
import logging
import sys
from program_wrapper import ProgramWrapper


if __name__ == "__main__":
    logger = logging.getLogger("mylog")
    logger.setLevel(10)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    PW = ProgramWrapper("tail -f a.txt", logger)
    PW.start()
    

ubuntu@dev:~/myprojects/program_wrapper$ python test.py
```
##demo2
```bash
ubuntu@dev:~/myprojects/program_wrapper$ python program_wrapper.py -c "tail -f a.txt"
```
#DESCRIPTION
提供一个程序，将其包装为子进程，捕获其标准输出和标准错误到指定的log文件<br/>
