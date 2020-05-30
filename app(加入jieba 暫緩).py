from flask import Flask, render_template, request # Python的web開發框架
from flask_cors import CORS # 解決Flask跨來源資源共用問題(CORS)
from chatterbot import ChatBot 
from chatterbot.trainers import ChatterBotCorpusTrainer #
from OpenSSL import SSL
import gc  # Python內部垃圾蒐集回收(Garbage Collection)
# import jieba
# import jieba.posseg as pseg
# import jieba.analyse

app = Flask(__name__)
CORS(app)

bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("data/learning_corpus") #train the bot
bot.read_only = True #if True, bot will NOT learning after training
bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")

import process_model as pm #import emotion recognition model

@app.route("/") 
def home():
    return render_template("index.html") #display index

@app.route("/get", methods=['GET']) 
def get_bot_response():
    userText = request.args.get('msg')
    processed_text = pm.response(userText) #get text emotion prediction
    gc.collect()
    # # Jieba
    # jieba.set_dictionary('jieba\jieba\dict.txt.big') # 引入斷詞辭典
    # # jieba.load_userdict('jieba\jieba\dict.txt')
    # content = (userText) # 欲斷的語句
    # print ("輸入：", content) # 輸入語句
    # words = pseg.cut(content) #進行斷詞
    # print ("輸出 精確模式 Full Mode：") # 輸出斷詞結果
    # for word, flag in words:
    #     print('%s %s' % (word, flag))

    return (str(bot.get_response(userText)) + '   #' + processed_text + '')
    # return (str(bot.get_response(userText)) )

if __name__ == "__main__":
    context = ('certificate.crt', 'private.key')
    app.run(host='localhost',port=5000, ssl_context=context, threaded=True, debug=True)


