
# coding: utf-8

# In[22]:

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
    print(''.join(translate_results))
    return
    translate_results=process(Request_URL,Form_Data)
    #找到翻译结果
    if 'out' in translate_results['content']:
        translate_results = translate_results['content']['out']
    else:
        translate_results = translate_results['content']['word_mean']
    #打印翻译信息
    print(''.join(translate_results))


# In[26]:

Jinshan('abbr')


# In[ ]:



