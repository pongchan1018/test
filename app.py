from flask import Flask, render_template, request 
from flask_cors import CORS 
from chatterbot import ChatBot 
from chatterbot.trainers import ChatterBotCorpusTrainer #
from OpenSSL import SSL
import gc  # Python內部垃圾蒐集回收(Garbage Collection)

app = Flask(__name__)
CORS(app)

bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("data/learning_corpus") #train the bot
bot.read_only = True #if True, bot will NOT learning after training

bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")

import process_model as pm # 引入情感運算模型

@app.route("/") 
def home():
    return render_template("index.html") #display index

@app.route("/get", methods=['GET']) 
def get_bot_response():
    userText = request.args.get('msg')
    processed_text = pm.response(userText) #get text emotion prediction
    gc.collect()
    return (str(bot.get_response(userText)) + '   #' + processed_text + '')

if __name__ == "__main__":
    context = ('certificate.crt', 'private.key')
    app.run(host='localhost',port=5000, ssl_context=context, threaded=True, debug=True)