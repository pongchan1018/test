# -*- coding: utf-8 -*-
import os, requests, uuid, json

# 檢查以確保翻譯器文本訂閱密鑰是否可作為環境變量使用。
# 如果您將訂閱密鑰設置為字符串，請註釋這幾行。
"""
if 'TRANSLATOR_TEXT_KEY' in os.environ:
    subscriptionKey = os.environ['TRANSLATOR_TEXT_KEY']

else:
    print('Environment variable for TRANSLATOR_TEXT_KEY is not set.')
    exit()
"""
# 如果要將訂閱密鑰設置為字符串，請取消註釋下面的行並添加訂閱密鑰。
subscriptionKey = '079ee590202b482c9006b9be5f3bbe1b'
# 臨時替換


base_url = 'https://api.cognitive.microsofttranslator.com'
path = '/translate?api-version=3.0'
params = '&to=en'
constructed_url = base_url + path + params
def get_trans(text): # 調用 微軟Bing API 進行英語翻譯
    headers = {
        'Ocp-Apim-Subscription-Key': subscriptionKey,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{
        'text' : text
    }]

    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()

    #print(json.dumps(response, sort_keys=True, indent=4, ensure_ascii=False, separators=(',', ': ')))
    return response[0]['translations'][0]['text']


