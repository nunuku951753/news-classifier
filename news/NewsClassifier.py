#!/usr/bin/env python
# coding: utf-8

# ### Data Preprocessing ###

# In[3]:


import re
import jieba
import jieba.analyse
import keras
import pandas as pd
import numpy as np
from pythonbq import pythonbq
from keras.models import load_model

class NewsClassifier():

    def __init__(self, model_path):
        self.model = load_model(model_path)
        
    # 取字詞資料集並匯出csv
    def getWord_index_csv(self):
        my_project_id='maximal-cabinet-254805'
        my_dataset_id='news_keywords'
        credentials_path = 'C:/Users/GameToGo/MyCredentials/My First Project-7226ff9d97d3.json'
        
        myProject=pythonbq(
          bq_key_path = credentials_path,
          project_id = my_project_id
        )
        SQL_CODE="""
            SELECT * FROM `maximal-cabinet-254805.news_keywords.keywords` 
            order by id
        """

        output=myProject.query(sql=SQL_CODE)
        output.to_csv('word_index.csv', index = False)

    # 讀取字詞集csv
    def getWord_index(self):
        word_df = pd.read_csv('./news/word_index.csv')

        word_index = {}
        for w in word_df.values:
            word_index[w[1]] = w[0]

        return word_index

    # 關鍵字提取(基于TF-IDF算法)
    def getTxtArray(self, txt, K, word_index):
        pattern = re.compile(r'[\d+\u4e00-\u9fa5]+') # 取中文加數字
        txt_list = pattern.findall(txt)
        txt2 = ''.join(txt_list)

        keywords = jieba.analyse.extract_tags(
                            sentence=txt2, topK=K, withWeight=True, allowPOS=('n','nr','ns'))
        words = []
        txt_index = []
        for item in keywords:
            key = item[0]
            words.append(key)
            if key in word_index.keys():
                txt_index.append(word_index[key])   
            else:
                txt_index.append(0) 
        
        return words, [txt_index]
    
    # 匯入model與預測
    def getPredictAns(self, txt):
        s = ["政治", "運動", "財經", "社會", "房產", "國際", "娛樂"]
        
        word_index = self.getWord_index()
        words, txt_index = self.getTxtArray(txt, 20, word_index)
        # 關鍵字不滿20補0
        txt_seq = keras.preprocessing.sequence.pad_sequences(txt_index, maxlen = 20)
        
        pre = self.model.predict(txt_seq)
        ans = pre.argmax(axis=1)[0]
        return words, ans


# In[4]:


# txt = "第92屆奧斯卡金像獎頒獎典禮於台灣時間今（10）日早上9點於洛杉磯舉行，今年電影每一部都令人驚豔，《寄生上流》、《小丑》、《1917》等大片都備受矚目。本屆頒獎典禮比照去年沒有主持人，眾多好萊塢巨星輪番上陣，每一位表演者都令人期待。稍早頒發的第一個最佳男配角，由《從前，有個好萊塢》的布萊德彼特奪下、《婚姻故事》蘿拉鄧恩奪最佳女配角。韓國電影《寄生上流》入圍最佳影片、導演、國際電影等6項大獎，最具話題性，拿下最佳影片獎、最佳原創劇本獎、最佳國際影片和最佳導演，最佳男主角和最佳女主角分別由《小丑》瓦昆菲尼克斯、《茱蒂》芮妮齊薇格奪得。"

# classifier = NewsClassifier('./model/7news_lstm_acc89.h5')
# words, ans = NewsClassifier.getPredictAns(classifier, txt)
# print(ans)
# print(words)

