from keras.models import load_model # 直接載入之前訓練好的模型
from keras.preprocessing.sequence import pad_sequences 
# keras只能接受長度相同的序列輸入。為解決序列長度參差不齊，便需要使用pad_sequences()。
# 該函數是將序列轉化爲經過填充以後的一個長度相同的新序列(截長補短)
import keras # 用Python編寫的開源神經網路庫
import pickle 
import tensorflow as tf
from ms_translator import get_trans

gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.8) # 只使用50%的GPU記憶體
sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options)) 
# Launch the graph in a session that allows soft device placement and
# logs the placement decisions.
sess = keras.backend.get_session()
init = tf.compat.v1.global_variables_initializer()
sess.run(init)

MAX_SEQUENCE_LENGTH = 30  # 文本（文字）的最大長度（包括空格）

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle) # Keras文本預處理-Loading

classes = ["neutral", "happy", "sad", "hate","anger"] # 情緒分類

model = load_model('checkpoint-0.912.h5') # 已訓練好的模型
model._make_predict_function()

def response(text):
    with sess.as_default():
        text = get_trans(text) # 中翻英
        text = [text] 
        sequences_test = tokenizer.texts_to_sequences(text)
        data_int_t = pad_sequences(sequences_test, padding='pre', maxlen=(MAX_SEQUENCE_LENGTH-5))
        data_test = pad_sequences(data_int_t, padding='post', maxlen=(MAX_SEQUENCE_LENGTH))
        y_prob = model.predict(data_test)
        for n, prediction in enumerate(y_prob):
            pred = y_prob.argmax(axis=-1)[n]
            prediction = classes[pred]
        return prediction