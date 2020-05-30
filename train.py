from chatterbot import ChatBot 
from chatterbot.trainers import ChatterBotCorpusTrainer 

bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("data/learning_corpus") #train the bot
bot.read_only = True #if True, bot will NOT learning after training