from flask import Flask, request, abort, render_template

import openai
import os
import requests
import json
from datetime import datetime
#import time
#import logging

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from foodlist import checkfoodlist

app = Flask(__name__)
#logging.basicConfig(filename='record.log', level=logging.INFO)

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN',  None), timeout=30)
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET',  None))
chatGPT_key = os.getenv('AI_APIKEY', None)
weather_token = os.getenv('WEATHER_TOKEN', None)

def lineNotifyWeather(token, msg):
    token = weather_token
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"}

    NowDate = datetime.now().strftime('%Y-%m-%d')
    print(NowDate)
    NowTime = NowDate + 'T06:00:00'

    Location_List = ['臺北市', '新北市', '桃園市', '基隆市']
    msg = "\r    時間: 6:00~18:00\r"
    msg_weather = ''

    for i in Location_List[0:]:
        cwbapi = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-E74B046A-CAB4-4570-B4D9-FA3F7F225DC1&locationName={i}&startTime="
        cwbr = requests.get(cwbapi)
        print('request success!!')

        cwbr_dict = cwbr.json()
        json_string = json.dumps(cwbr_dict)
        json_format = json.loads(json_string)
        location = json_format['records']['location'][0]['locationName']
        weather = json_format['records']['location'][0]['weatherElement'][0]['time'][0]['parameter']['parameterName']
        MinT = json_format['records']['location'][0]['weatherElement'][2]['time'][0]['parameter']['parameterName']
        MaxT = json_format['records']['location'][0]['weatherElement'][4]['time'][0]['parameter']['parameterName']
        pop = json_format['records']['location'][0]['weatherElement'][1]['time'][0]['parameter']['parameterName']
        msg_weather = msg_weather + f'''
        
    {location}: {weather}
    氣溫: {MinT}度~{MaxT}度
    降雨機率: {pop}%'''

    payload = {'message': msg + msg_weather}

    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=payload)
    return r.status_code

def check_group_or_user(eventsource):
    if hasattr(eventsource, "group_id"):
        return eventsource.group_id
    else:
        return eventsource.user_id
    

# 喚醒heroku
@app.route("/")
def home():
    return render_template("home.html")

# Line Notify
@app.route("/test", methods=['GET'])
def test():
    values = request.args.get('value')
    # return  lineNotifyMessage('1',values)
    status_code = lineNotifyWeather('1', values)
    return 'OK'

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.debug("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#加入群組自動發送
@handler.add(JoinEvent)
def handle_join(event):
    message = TextSendMessage(text=" 安安你好\n我只是個蒜頭，你問啥我就回答啥~\n輸入 \'請問蒜頭\'\n來獲得一些小建議\n-----\n若想再看一次此內容\n請輸入：\n!蒜頭自介")

    line_bot_api.reply_message(event.reply_token,message)
    print("JoinEvent =", JoinEvent)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    strCheck = str(event.message.text)
    print(strCheck)
    
    #不接收line官方的訊息
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        
        if strCheck == "!蒜頭自介" or strCheck == "！蒜頭自介":
         #            if strCheck.find('自我介紹') >= 0 :
            message = TextSendMessage(text=" 安安你好\n我只是個蒜頭，你問啥我就回答啥~\n輸入 \'請問蒜頭\'\n來獲得一些小建議\n-----\n若想再看一次此內容\n請輸入：\n!蒜頭自介")
            line_bot_api.reply_message(event.reply_token, message)

        #ChatGPT 回覆            
        elif strCheck.find('請問蒜頭') == 0:
            openai.api_key = chatGPT_key
            # 將第5個字元之後的訊息發送給 OpenAI
            prompt = strCheck[4:]
            event_id = check_group_or_user(event.source)
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',       #replace from 'text-davinci-003'
                messages=[
                    {'role': 'user', 'content': prompt}
                ],
                temperature=1.2
                #max_tokens = 1500
            )
            # 接收到回覆訊息後，移除換行符號
            reply_msg = response['choices'][0]['message']['content'].replace('\n', '')
            print(reply_msg)
            message = TextSendMessage(text=reply_msg)
            
            # 因為ChatGPT回復可能超過30秒(replytoken會失效)，所以改使用push api
            line_bot_api.push_message(event_id, message)
            #line_bot_api.reply_message(event.reply_token, message)

        elif strCheck.find('！公告 ') == 0 or strCheck.find('!公告 ') == 0: #geocoding test
            reply = checkfoodlist.lineNotifyAnnounce(event)

        # 幹話
        elif event.message.text == "好美":
            message = TextSendMessage(text="哪有你美")
            line_bot_api.reply_message(event.reply_token, message)
        elif event.message.text == "好阿":
            message = TextSendMessage(text="好阿")
            line_bot_api.reply_message(event.reply_token, message)
        elif event.message.text == "好啊":
            message = TextSendMessage(text="好啊")
            line_bot_api.reply_message(event.reply_token, message)
        elif event.message.text == "好":
            message = TextSendMessage(text="好")
            line_bot_api.reply_message(event.reply_token, message)
        elif event.message.text == "!!測試":
            message = TextSendMessage(text="測試成功!")
            event_id = check_group_or_user(event.source)
            print(event_id)
            #time.sleep(31)
            line_bot_api.push_message(event_id, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
