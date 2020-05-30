from flask import Flask, render_template, request 
from flask_cors import CORS 
from chatterbot import ChatBot 
from chatterbot.trainers import ChatterBotCorpusTrainer #
from OpenSSL import SSL
import gc  # Python內部垃圾蒐集回收(Garbage Collection)
import pandas as pd
import jieba
import jieba.analyse
import jieba.posseg as pseg
import re

app = Flask(__name__)
CORS(app)

bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("data/learning_corpus") #train the bot
bot.read_only = True #if True, bot will NOT learning after training

bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")

sentment_table = pd.read_excel('VAD-Lexicon.xlsx')  # 匯入情緒辭典
# sentment_table.drop(['Unnamed: 10','Unnamed: 11'],inplace=True,axis=1)
all_table = pd.read_excel('VAD-Lexicon.xlsx',sheet_name='sheetALL') # 定義工作表

val_dict = dict(zip(list(all_table.word),list(all_table.Valence))) # 讀取Valence
aro_dict = dict(zip(list(all_table.word),list(all_table.Arousal))) # 讀取Arousal
dom_dict = dict(zip(list(all_table.word),list(all_table.Dominance))) # 讀取Dominance
sentment_dict={**val_dict}
sentment_dict1={**aro_dict}
sentment_dict2={**dom_dict}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    
    return False
# 藉由自定義函數is_number()方法來判斷字符串是否為數字

for v in sentment_dict.keys():
    if is_number(v):
        pass
    else:
        jieba.suggest_freq(v,True)

for a in sentment_dict1.keys():
    if is_number(a):
        pass
    else:
        jieba.suggest_freq(a,True)

for d in sentment_dict2.keys():
    if is_number(d):
        pass
    else:
        jieba.suggest_freq(d,True)
# 把不是數字的字典的單字加進結巴分詞

stop_words = [re.findall(r'\S+',v)[0] for v in open('stopwords_ch.txt',encoding='utf8').readlines() if len(re.findall(r'\S+',v))>0]
def Vsent2word(sentence,stop_words=stop_words):
    words = jieba.cut(sentence, HMM=False)
    words = [v for v in words if v not in stop_words]
    return words

stop_words = [re.findall(r'\S+',a)[0] for a in open('stopwords_ch.txt',encoding='utf8').readlines() if len(re.findall(r'\S+',a))>0]
def Asent2word(sentence,stop_words=stop_words):
    words = jieba.cut(sentence, HMM=False)
    words = [a for a in words if a not in stop_words]
    return words

stop_words = [re.findall(r'\S+',d)[0] for d in open('stopwords_ch.txt',encoding='utf8').readlines() if len(re.findall(r'\S+',d))>0]
def Dsent2word(sentence,stop_words=stop_words):
    words = jieba.cut(sentence, HMM=False)
    words = [d for d in words if d not in stop_words]
    return words
# 準備斷詞和停止詞

@app.route("/") 
def home():
    return render_template("index.html") #display index

@app.route("/get", methods=['GET']) 
def get_bot_response():
    userText = request.args.get('msg')

    def get_sentment(userText):
        tokens = Vsent2word(userText) # 斷詞
        Vscore = 0  # V情緒分數
        countword = 0 # 詞塊數量
        for v in tokens: # 從tokens(斷詞)中取得元素執行v，直到元素取完為止
            if v in sentment_dict.keys(): 
                Vscore += sentment_dict[v]
                countword += 1
        if countword != 0:
            print(Vscore/countword)
        else:
            return 0
        
        tokens = Asent2word(userText) # 斷詞
        Ascore = 0  # A情緒分數
        countword1 = 0 # 詞塊數量
        for a in tokens: # 從tokens(斷詞)中取得元素執行a，直到元素取完為止
            if a in sentment_dict1.keys(): 
                Ascore += sentment_dict1[a]
                countword1 += 1
        if countword1 != 0:
            print(Ascore/countword1)
        else:
            return 0

        tokens = Dsent2word(userText) # 斷詞
        Dscore = 0  # D情緒分數
        countword2 = 0 # 詞塊數量
        for d in tokens: # 從tokens(斷詞)中取得元素執行d，直到元素取完為止
            if d in sentment_dict2.keys(): 
                Dscore += sentment_dict2[d]
                countword2 += 1
        if countword != 0:
            print(Dscore/countword2)
            score = (Vscore/countword,Dscore/countword1,Dscore/countword2)

            if  0 <= Vscore/countword <= 0.2 and 0.65 <= Ascore/countword1 <= 0.85 and 0 <= Dscore/countword2 <= 0.45:  
                emotion = 'fear'
            elif  0.05 <= Vscore/countword <= 0.25 and 0.7 <= Ascore/countword1 <= 0.9 and 0.55 <= Dscore/countword2 <= 1:  
                emotion = 'angry'
            elif  0.2 <= Vscore/countword <= 0.4 and 0.65 <= Ascore/countword1 <= 0.85 and 0 <= Dscore/countword2 <= 0.45:  
                emotion = 'disgust'
            elif  0.5 <= Vscore/countword <= 0.35 and 0.5 <= Ascore/countword1 <= 0.35 and 0 <= Dscore/countword2 <= 0.4:  
                emotion = 'sad'
            elif  0.7 <= Vscore/countword <= 1 and 0.5 <= Ascore/countword1 <= 0.75 and 0.5 <= Dscore/countword2 <= 0.85:  
                emotion = 'happy'
            elif  0.6 <= Vscore/countword <= 0.9 and 0.75 <= Ascore/countword1 <= 1 and 0.45 <= Dscore/countword2 <= 0.65:  
                emotion = 'surprise'
            else:
                emotion = 'neutral'
            print("該句的三維VAD數值分別為：",score)
            print("該句情緒判斷為：",emotion)
        else:
            return 0
    
    get_sentment(userText)

    gc.collect()
    return (str(bot.get_response(userText)) )

if __name__ == "__main__":
    context = ('certificate.crt', 'private.key')
    app.run(host='localhost',port=5000, ssl_context=context, threaded=True, debug=True)