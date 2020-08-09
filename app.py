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
# import logging


app = Flask(__name__)
CORS(app)

bot = ChatBot(
    "Chatterbot", 
    storage_adapter = "chatterbot.storage.SQLStorageAdapter",
    input_adapter = 'chatterbot.input.VariableInputTypeAdapter',
    output_adapter = 'chatterbot.output.TerminalAdapter',
    # logic_adapters = [
    #     {
    #         "import_path":"chatterbot.logic.BestMatch",
    #         "statement_comparison_function":"chatterbot.comparisons.levenshtein_distance",
    #         "response_selection_method":"chatterbot.response_selection.get_first_response"
    #     },
    #     {
    #         "import_path":"chatterbot.logic.MathematicalEvaluation"
    #     },
    #     {
    #         "import_path":"chatterbot.logic.TimeLogicAdapter"
    #     },
    #     {
    #         "import_path":"chatterbot.logic.LowConfidenceAdapter",
    #         "threshold":0.5,
    #         "default_response":"什么鬼？"
    #     }
    # ],
    preprocessors = [
        'chatterbot.preprocessors.clean_whitespace'
    ],
    filters=[
        'chatterbot.filters.RepetitiveResponseFilter'
    ],
    # database_uri = "postgres://kdopzajlwqjyoc:72ec00eb4d3374b5857f0a23bc5d8547795ccd1ab48848d00112973bb3fe2e4b@ec2-50-16-198-4.compute-1.amazonaws.com:5432/df6ipclmd9tuph",
    database_uri = "sqlite:///database_test.db",
    database = "db_chatterbot"
    )
#trainer = ChatterBotCorpusTrainer(bot)
#trainer.train("data/learning_corpus") #train the bot
# bot.read_only = True #if True, bot will NOT learning after training

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
            print(tokens)
            non_count = userText.count("沒有")+userText.count("不是")+userText.count("無")+userText.count("大可不必")+userText.count("犯不著")+userText.count("不可以")+userText.count("不可")+userText.count("不能")+userText.count("不再")+userText.count("不得")+userText.count("不行")+userText.count("不准")+userText.count("不許")+userText.count("不必")+userText.count("不用")+userText.count("不須")+userText.count("絕不")+userText.count("決不")+userText.count("犯不著")+userText.count("不可以")+userText.count("不可")+userText.count("不能")+userText.count("不再")+userText.count("不得")+userText.count("不行")+userText.count("不准")+userText.count("不許")+userText.count("不必")+userText.count("不用")+userText.count("不須")+userText.count("絕不")+userText.count("決不")+userText.count("並非")+userText.count("從不")+userText.count("從未")+userText.count("毫不")+userText.count("毫無")+userText.count("絕非")+userText.count("無法")
            if (non_count % 2) == 1:
                print("否定詞有",non_count,"個，是奇數，該句為否定句")
                valence_score = 1-(Vscore/countword)
                arousal_score = 1-(Ascore/countword1)
                dominance_score = 1-(Dscore/countword2)
                Gscore = (valence_score,arousal_score,dominance_score)
                print("該句為否定句，VAD數值為：",Gscore)

                Gscore = (valence_score,arousal_score,dominance_score)
                if  0 <= valence_score <= 0.3 and 0.62 <= arousal_score <= 0.92 and 0.19 <= dominance_score <= 0.49:  
                    emotion = 'fear'
                elif  0.04 <= valence_score <= 0.34 and 0.6 <= arousal_score <= 0.9 and 0.37 <= dominance_score <= 0.67:  
                    emotion = 'angry'
                elif  0 <= valence_score <= 0.3 and 0.28 <= arousal_score <= 0.58 and 0.187 <= dominance_score <= 0.487:  
                    emotion = 'disgust'
                elif  0 <= valence_score <= 0.3 and 0.4 <= arousal_score <= 0.7 and 0.1 <= dominance_score <= 0.4:  
                    emotion = 'sad'
                elif  0.7 <= valence_score <= 1 and 0.59 <= arousal_score <= 0.89 and 0.57 <= dominance_score <= 0.87:  
                    emotion = 'happy'
                elif  0.67 <= valence_score <= 0.97 and 0.67 <= arousal_score <= 0.97 and 0.47 <= dominance_score <= 0.77:  
                    emotion = 'surprise'
                else:
                    emotion = 'neutral'
                print("該否定句的情緒判斷為：",emotion)

            else:
                print("否定詞有",non_count,"個，是偶數，故該句為肯定句或雙重否定")
                valence_score = Vscore/countword
                arousal_score = Ascore/countword1
                dominance_score = Dscore/countword2
                score = (valence_score,arousal_score,dominance_score)
                print("該句為肯定句，VAD數值為：",score)
                score = (valence_score,arousal_score,dominance_score)
                if  0 <= valence_score <= 0.3 and 0.62 <= arousal_score <= 0.92 and 0.19 <= dominance_score <= 0.49:  
                    emotion = 'fear'
                elif  0.04 <= valence_score <= 0.34 and 0.6 <= arousal_score <= 0.9 and 0.37 <= dominance_score <= 0.67:  
                    emotion = 'angry'
                elif  0 <= valence_score <= 0.3 and 0.28 <= arousal_score <= 0.58 and 0.187 <= dominance_score <= 0.487:  
                    emotion = 'disgust'
                elif  0 <= valence_score <= 0.3 and 0.4 <= arousal_score <= 0.7 and 0.1 <= dominance_score <= 0.4:  
                    emotion = 'sad'
                elif  0.7 <= valence_score <= 1 and 0.59 <= arousal_score <= 0.89 and 0.57 <= dominance_score <= 0.87:  
                    emotion = 'happy'
                elif  0.67 <= valence_score <= 0.97 and 0.67 <= arousal_score <= 0.97 and 0.47 <= dominance_score <= 0.77:  
                    emotion = 'surprise'
                else:
                    emotion = 'neutral'
                print("該肯定句的情緒判斷為：",emotion)
        else:
            return 0
    
    get_sentment(userText)

    gc.collect()
    return (str(bot.get_response(userText)) )

if __name__ == "__main__":
    context = ('certificate.crt', 'private.key')
    app.run(host='localhost',port=5000, ssl_context=context, threaded=True, debug=True)
