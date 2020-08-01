import pandas as pd
import jieba
import jieba.analyse
import jieba.posseg as pseg
import re

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


def get_sentment(sent):
    tokens = Vsent2word(sent) # 斷詞
    Vscore = 0  # V情緒分數
    countword = 0 # 詞塊數量
    print('Valence')
    for v in tokens: # 從tokens(斷詞)中取得元素執行v，直到元素取完為止
        if v in sentment_dict.keys(): 
            Vscore += sentment_dict[v]
            countword += 1
            print(v,end='')
            print(sentment_dict[v])      
    if countword != 0:
        print('Valence的平均分數為:',Vscore/countword)
        print('___________________________')
    else:
        return 0

    tokens = Asent2word(sent) # 斷詞
    Ascore = 0  # A情緒分數
    countword1 = 0 # 詞塊數量
    print('Arousal')
    for a in tokens: # 從tokens(斷詞)中取得元素執行a，直到元素取完為止
        if a in sentment_dict1.keys(): 
            Ascore += sentment_dict1[a]
            countword1 += 1
            print(a,end='')
            print(sentment_dict1[a])
    if countword != 0:
        print('Arousal的平均分數為:',Ascore/countword1)
        print('___________________________')
    else:
        return 0

    tokens = Dsent2word(sent) # 斷詞
    Dscore = 0  # D情緒分數
    countword2 = 0 # 詞塊數量
    print('Dominance')
    for d in tokens: # 從tokens(斷詞)中取得元素執行d，直到元素取完為止
        if d in sentment_dict2.keys(): 
            Dscore += sentment_dict2[d]
            countword2 += 1
            print(d,end='')
            print(sentment_dict2[d])
    if countword != 0:
        print('Dominance的平均分數為:',Dscore/countword2)
        print('___________________________')
        print(tokens)
        # num = sent.count("沒有"),sent.count("不是"),sent.count("無"),sent.count("大可不必"),sent.count("犯不著"),sent.count("不可以"),sent.count("不可"),sent.count("不能"),sent.count("不再"),sent.count("不得"),sent.count("不行"),sent.count("不准"),sent.count("不許"),sent.count("不必"),sent.count("不用"),sent.count("不須"),sent.count("絕不"),sent.count("決不"),sent.count("犯不著"),sent.count("不可以"),sent.count("不可"),sent.count("不能"),sent.count("不再"),sent.count("不得"),sent.count("不行"),sent.count("不准"),sent.count("不許"),sent.count("不必"),sent.count("不用"),sent.count("不須"),sent.count("絕不"),sent.count("決不"),sent.count("並非"),sent.count("從不"),sent.count("從未"),sent.count("毫不"),sent.count("毫無"),sent.count("絕非"),sent.count("無法")
        # print (num)
        non_count = sent.count("沒有")+sent.count("不是")+sent.count("無")+sent.count("大可不必")+sent.count("犯不著")+sent.count("不可以")+sent.count("不可")+sent.count("不能")+sent.count("不再")+sent.count("不得")+sent.count("不行")+sent.count("不准")+sent.count("不許")+sent.count("不必")+sent.count("不用")+sent.count("不須")+sent.count("絕不")+sent.count("決不")+sent.count("犯不著")+sent.count("不可以")+sent.count("不可")+sent.count("不能")+sent.count("不再")+sent.count("不得")+sent.count("不行")+sent.count("不准")+sent.count("不許")+sent.count("不必")+sent.count("不用")+sent.count("不須")+sent.count("絕不")+sent.count("決不")+sent.count("並非")+sent.count("從不")+sent.count("從未")+sent.count("毫不")+sent.count("毫無")+sent.count("絕非")+sent.count("無法")
        # print (non_count)
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
            print("該句情緒判斷為：",emotion)

        else:
            print("否定詞有",non_count,"個，是偶數，故該句為肯定句或雙重否定")
            valence_score = Vscore/countword
            arousal_score = Ascore/countword1
            dominance_score = Dscore/countword2
            score = (valence_score,arousal_score,dominance_score)
            print("該句為直述句，VAD數值為：",score)
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
            print("該句情緒判斷為：",emotion)
    else:
        return 0
    
sent ="我是開心"
get_sentment(sent)

