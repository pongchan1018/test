#encoding=utf-8
import jieba
import jieba.posseg as pseg

jieba.set_dictionary('jieba-master/extra_dict/dict.txt.big')

content = open('jieba-master/extra_dict/article.txt', 'rb').read()

print ("Input：", content)

words = pseg.cut(content)

print ("Output 精確模式 Full Mode：")
for word in words:
    print (word.word, word.flag)