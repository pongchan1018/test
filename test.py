import jieba
import jieba.analyse
import jieba.posseg as pseg


# jieba.set_dictionary('jieba/jieba/dict.txt')
# jieba.load_userdict("jieba/jieba/dict.txt")
s = "我現在的心情非常好"
words = pseg.cut(s)
for word, flag in words:
    print('%s %s' % (word, flag))