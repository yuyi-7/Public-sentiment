import re
import pyodbc
import numpy as np
import pandas as pd
import jieba
from gensim import corpora,models

stoppath = r'stoplist.txt'

def createfilter():
    filterlist = []

    filterlist.append(re.compile('的秒拍视频'))
    filterlist.append(re.compile('展开全文c'))

    return filterlist


def filter(filterlist,data):
    first = [filterlist[0].split(x)[0] for x in data]
    second = [filterlist[1].split(x)[0] for x in first]
    del(first)
    return second


def connect():
    print('正在连接数据库...')
    conn = pyodbc.connect(r'DRIVER={SQL Native Client};SERVER=119.23.53.26,3389\sql05;DATABASE=YQweibodata;UID=sa;PWD=Zhkj_123')
    print('已连接数据库')
    cursor = conn.cursor()
    return cursor


def gettables(cursor):
    cursor.execute('SELECT * FROM INFORMATION_SCHEMA.TABLES')
    row = cursor.fetchall()
    tables = [x[2] for x in row]
    print('获取的表有：')
    print(tables)
    del(row)
    return tables


def getcleandata(cursor,tables):
    data = []
    filterlist = createfilter()  #建立过滤器

    for i in range(len(tables)):
        cursor.execute('select * from %s'%tables[i])
        print('连接到表：%s'%tables[i])

        row = cursor.fetchall()

        textpattern = re.compile(r'\w')
        text = [''.join(textpattern.findall(x[3])) for x in row]
        text = filter(filterlist,text)  #过滤一些干扰词
        print('已经过滤掉表%s中的干扰句'%tables[i])

        for j in text:
            data.append(j)
        print('已添加到当前内存中，数据大小为：%d'%len(data))

    data = np.array(data)
    print('获得的数据大小为:')
    print(data.shape)
    return data


def fenci(data):
    data = pd.DataFrame(data)
    #text_fenci = [r' '.join(jieba.cut(x)) for x in data]
    data[1] = data[0].apply(lambda x:' '.join(jieba.cut(x)))
    data[2] = data[1].apply(lambda x: x.split(' '))
    print('成功分词')

    print('正在读取停词表...')
    stop = pd.read_csv(stoppath,encoding='utf-8',header=None,sep='tipdm',engine='python')
    print('已经读取停词表')
    
    print('正在过滤掉停用词...')
    stop = [' ',''] + list(stop[0])
    data[3] = data[2].apply(lambda x:[i for i in x if i not in stop])
    print('成功过滤停用词')
    return data[3]

def anayle(data,topic_num):
    print('开始建模...')
    text_dict = corpora.Dictionary(data)  #建立词典
    text_corpus = [text_dict.doc2bow(i) for i in data]  #建立语料库

    lda = models.LdaModel(text_corpus,num_topics=topic_num,id2word=text_dict)

    print('分析成功,得到的主题有：')
    for i in range(topic_num):
        print(lda.print_topic(i))


if __name__=='__main__':
    cursor = connect()
    tables = gettables(cursor)
    data = getcleandata(cursor,tables)
    data = fenci(data)
    anayle(data,10)