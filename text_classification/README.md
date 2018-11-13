# 代码介绍

这里使用的文本分类代码*LDA.py*，还使用了*stoplist.txt*作为停用词列表

### LDA.py

这里介绍一下代码的使用方法：

本程序要用到的python库有：

```python
import re
import pyodbc
import numpy as np
import pandas as pd
import jieba
from gensim import corpora,models
```

所以需要先安装好以上几个库，另外，对于**pyodbc**库，需要去下载**SQL Server 2005**的驱动器SQL Native Client，最简单的方法就是安装一个SQL Server 2005

在程序的最后有以下代码：

```python
if __name__=='__main__':  #判断是否在运行本程序
    cursor = connect()  #连接数据库，返回游标
    tables = gettables(cursor)  #获取数据库中的所有表名
    data = getcleandata(cursor,tables)  #获取文本并清楚掉过滤表中的干扰句
    data = fenci(data)  #分词
    anayle(data,10)  #建立模型并输出分类结果，第二个参数是预设的聚类簇数
```

可以修改程序中的聚类簇数，直接运行程序即可

**输出结果**为所有类别的主题以及其主题概率

## stoplist.txt

该文件是存放中文停用词的文件，程序会自动读取该文件并把文本中的所有包含有该文件的词都去掉，以提高模型的聚类效果，但仍需补充。

---

### LDA模型

本程序用到的模型是**LDA模型**，该模型是一种概率模型，可以视为一种无监督的贝叶斯模型。也是一种典型的词袋模型。

LDA算法开始时，先随机地给θd，ϕt赋值(对所有的d和t)

针对特定的文档ds中的第i单词wi，如果令该单词对应的主题为tj，可以写出公式为:

Pj(wi|ds)=P(wi|tj)∗P(tj|ds)

枚举T中的主题，得到所有的Pj(wi|ds).然后可以根据这些概率值的结果为ds中的第i个单词wi选择一个主题，最简单的就是取令Pj(wi|ds)概率最大的主题 tj。

如果ds中的第i个单词wi在这里选择了一个与原先不同的主题，就会对θd，ϕt有影响，他们的影响反过来影响对上面提到的p(w|d)的计算。
