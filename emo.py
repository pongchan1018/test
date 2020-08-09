import pandas as pd
import jieba
import jieba.analyse
import jieba.posseg as pseg
import re


sentment_table = pd.read_excel('VAD-Lexicon.xlsx') 
# sentment_table.drop(['Unnamed: 10','Unnamed: 11'],inplace=True,axis=1)
pos_table = pd.read_excel('VAD-Lexicon.xlsx',sheet_name='sheetPOS')
neg_table = pd.read_excel('VAD-Lexicon.xlsx',sheet_name='sheetNEG')

pos_dict = dict(zip(list(pos_table.posword),list(pos_table.Vscore)))
neg_dict = dict(zip(list(neg_table.negword),list(neg_table.Vscore)))

# neg_dict = dict(zip(list(neg_table.negword),map(lambda a:a*(0-1),list(neg_table.vscore)) ))
sentment_dict={**pos_dict,**neg_dict}

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

for w in sentment_dict.keys():
    if is_number(w):
        pass
    else:
        jieba.suggest_freq(w,True)

stop_words = [re.findall(r'\S+',w)[0] for w in open('stopwords_ch.txt',encoding='utf8').readlines() if len(re.findall(r'\S+',w))>0]
def sent2word(sentence,stop_words=stop_words):
    words = jieba.cut(sentence, HMM=False)
    words = [w for w in words if w not in stop_words]
    return words

def get_sentment(sent):
    tokens = sent2word(sent)
    score = 0
    countword = 0
    for w in tokens:
        if w in sentment_dict.keys():
            score += sentment_dict[w]
            countword += 1
            print(w,end='')
            print(sentment_dict[w])
    if countword != 0:
        print(score/countword)
    else:
        return 0

sent ="今天是個快樂又滿足的一天"
get_sentment(sent)
