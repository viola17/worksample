
# coding: utf-8

# In[2]:
import pickle
import sys
import nltk
from pomegranate import *


# In[3]:


with open('pair.pkl','rb') as f:
    pair = pickle.load(f)[0:50]


# In[4]:


w = [] #所有出现的词
p = [] #所有词性

for i in pair:
    for j in i:
        w.append(j[0])
        p.append(j[1])
#print(w[0:40])
#print(p[0:40])
#print(pair[0:2])


# In[5]:


from collections import defaultdict
#每个词的词性list
w_p = defaultdict(list)
for i in range(len(w)):
    w_p[w[i]].append(p[i])

#每个词性对应list of words
p_w = defaultdict(list)
for i in range(len(w)):
    p_w[p[i]].append(w[i])


# In[6]:


w_dic2 = {}
for i in w_p:
    p_dic2 = {}
    for j in w_p[i]:
        p_dic2[j]=w_p[i].count(j)
    w_dic2[i] = p_dic2
#print(w_dic2)


p_dic1 = {}
for i in p_w:
    w_dic1 = {}
    for j in p_w[i]:
        w_dic1[j]=p_w[i].count(j)
    p_dic1[i] = w_dic1
#print(p_dic1)


# In[7]:


#emission matrix 
p_freq = {}
for i in p_dic1:
    p_count = 0
    word = {}
    for j in p_dic1[i]:
        p_count += p_dic1[i][j]
    for j in p_dic1[i]:
        word[j]=p_dic1[i][j]/p_count
    p_freq[i] = State(DiscreteDistribution(word),name = i)

#print(p_freq)


# In[8]:


model = HiddenMarkovModel('pos_tag')


# In[9]:


#共有词性多少个
count = 0
for i in p_dic1:
    for j in p_dic1[i]:
        count += p_dic1[i][j]

states = [] #pos tag
for i in p_freq:
    states.append(p_freq[i])
    
model.add_states(states)


# In[10]:


for i in p_freq:
    model.add_transition(model.start, p_freq[i], p.count(i)/count)


# In[11]:


#transition matrix
p_sentence =[]
for i in pair:
    p_string = []
    for j in i:
        p_string.append(j[1])   
    p_sentence.append(p_string)


# In[12]:


trans_prob = {}
for s in p_sentence:
    numerator =0
    for i in range(len(s)-1):
        first = s[i]
        second = s[i+1]
        denom = p.count(first)
    if any([first,second] == s[i:i+2] for i in range(len(s) - 1)):
        numerator += 1
    trans_prob[(first,second)] = numerator/denom


# In[13]:


for i in p_freq:
    for j in p_freq:
        if (i,j) not in trans_prob.keys():
            trans_prob[(i,j)] = 0
        model.add_transition(p_freq[i],p_freq[j],trans_prob[(i,j)])
model.bake()


# In[14]:


print(", ".join(state.name for i, state in model.viterbi(['\u7136','\u5148\u751f'])[1]))

