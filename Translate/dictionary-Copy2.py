
# coding: utf-8

# In[1]:

import pandas as pd
from pandas import DataFrame 
import re 
import urllib.parse
from hashlib import md5
import random
import json
import http.client
import urllib.request
from html.parser import HTMLParser


# In[4]:

import jieba
import socket
from scipy import spatial
import time
import pickle
from gensim import corpora, models, similarities
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import pandas as pd
import numpy as np
import inspect
import matplotlib.pyplot as plt
from datetime import datetime,timedelta,date
from jphelper import mysql_conn
connection = mysql_conn()
cursor = connection.cursor()
from pyhive import hive
connection2= hive.connect('10.81.237.42')
CMP_IDS =[524798, 100,1291,91572]
CMP_ID = 524798

#pd.set_option('display.max_rows',None)
#pd.set_option('display.max_colwidth',1000)
import http.client
import hashlib
import urllib.parse
import random
from urllib.request import urlopen
import json
import re
from urllib import request
from urllib import parse
import _md5


# In[23]:

def TranslateByBaidu(text, appid='20180822000197619', secretKey='O8uEcCPgSEs8HXwLgmdi', fromLang = 'auto',toLang = 'zh'):
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = text
    salt = random.randint(32768, 65536)

    sign1 = appid+q+str(salt)+secretKey
    sign =  hashlib.md5(sign1.encode("utf8")).hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
     
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        #response是HTTPResponse对象
        response = httpClient.getresponse()
        result = response.read()
        data = json.loads(result.decode('utf-8'))
        return data["trans_result"][0]["dst"]
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()



def unescape(text):
    parser = HTMLParser.HTMLParser()
    return (parser.unescape(text))


# In[24]:

def process(Request_URL,Form_Data):
    # 使用urlencode方法转换标准格式
    data = parse.urlencode(Form_Data).encode('utf-8')
    # 传递Request对象和转换完格式的数据
    response = request.urlopen(Request_URL, data)
    # 读取信息并解码
    html = response.read().decode('utf-8')
    # 使用JSON
    translate_results = json.loads(html)
    return  translate_results


# In[25]:

def Jinshan(word):
    Request_URL = 'http://fy.iciba.com/ajax.php?a=fy'
    #创建Form_Data字典，存储Form Data
    Form_Data = {'f' : 'auto',
                 't' : 'auto'}
    Form_Data['w']=word
    translate_results = process(Request_URL, Form_Data)
        # 找到翻译结果
    if 'out' in translate_results['content']:
        translate_results = translate_results['content']['out']
    else:
        translate_results = translate_results['content']['word_mean']
    # 打印翻译信息
 
    return ''.join(translate_results)
    translate_results=process(Request_URL,Form_Data)
    #找到翻译结果
    if 'out' in translate_results['content']:
        translate_results = translate_results['content']['out']
    else:
        translate_results = translate_results['content']['word_mean']
    #打印翻译信息
    return ''.join(translate_results)


#查语言function
import re
zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')

def getCh(st):
    global zh_pattern
    match = zh_pattern.search(st)
    return match

def containCh(st, minsize):
    if len(st)<minsize:
        return False
    global zh_pattern
    match = zh_pattern.search(st)
    if match==None:
        return False
    else:
        return True

def isEnWord(st, minsize):
    return st.encode( 'UTF-8' ).isalpha() & (len(st)>=minsize)


# In[8]:

job_position_by_date_sql = '''
select id as pid, title as pos_title, city as pos_city, company_id as cid,
employment_type as pos_employment_type, industry as pos_industry, language as pos_language, 
requirement as pos_requirement, accountabilities as pos_accountabilities
from jobdb.job_position where publish_date> "2017-01-01"
'''
job_pos_df= pd.read_sql_query(job_position_by_date_sql, connection)


# In[9]:

discard =[]
with open('stopwords.txt','r') as f:
    for l in f:
        p = l.strip().split('/n')
        discard += p


test = {}
dscp = job_pos_df['pos_requirement']#前一百个职位要求
low2 = []
for i in dscp:
    x2 = [x for x in jieba.cut(i) if len(x) >=2 and isEnWord(x,3)==True]    
    y2 = set(x2)
    #print(y1)
    #print(" ".join(y1))
    #print(" ".join(y1))
    for j in y2:
            c = j.lower()
            low2.append(c)
low2 = set(low2) 
count(dscp)


# In[ ]:

#对翻译结果进行切词的字典

test = {}
dscp = job_pos_df['pos_requirement']#前一百个职位要求
low2 = []
for i in dscp:
    x2 = [x for x in jieba.cut(i) if len(x) >=2 and isEnWord(x,3)==True]    
    y2 = set(x2)
    #print(y1)
    #print(" ".join(y1))
    #print(" ".join(y1))
    for j in y2:
            c = j.lower()
            low2.append(c)
low2 = set(low2) 

def is_chinese(ch):
#    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff' and len(ch)>=2 and ch!='过去分词':
             return True
        return False
    
for i in low2:
    if i not in discard:
            your_list2 = re.split('[;|a-zA-Z|.|,|&]', re.sub('\\（.*?）|\\{.*?}|\\[.*?]|\\〈.*?〉|\\<.*?>','',re.sub(r'\([^)]*\)','',Jinshan(i))))
            #for j in your_list2:
                #new = re.split('[;|a-zA-Z|.|，|&]',j)
            rejoin = list(jieba.cut(''.join(your_list2)))
            rejoin2 = [k for k in rejoin if is_chinese(k)]    
            test[i]= rejoin2


# In[532]:




# In[ ]:




# In[ ]:



