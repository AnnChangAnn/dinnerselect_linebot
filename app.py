import openai
import sys
import os
from flask import Flask, request, abort, render_template

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from foodlist import checkfoodlist

import random
import re
import urllib

import requests
import json
from datetime import datetime

app = Flask(__name__)

channel_secret = os.getenv('LINE_CHANNEL_SECRET',  None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN',  None)
chatGPT_key = os.getenv('AI_APIKEY', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)

if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

#喚醒heroku
@app.route("/")
def home():
    return render_template("home.html")

#Line Notify
@app.route("/test", methods=['GET'])
def test():
    values = request.args.get('value')
    #return  lineNotifyMessage('1',values)
    status_code = lineNotifyWeather('1',values)
    return '123'

def lineNotifyWeather(token, msg):
    #token = 'C2MMtPLrfSbUaTyaGWxZM7Zq58LwRKKoNjMfMWXtpGt' #國泰發行權杖
    #token = 'Q2bIg5ezRJOwgRm6pk6kSQeaKXw82OoPg2XzaTWPnwp' #cathaybk測試權杖
    #token = 'USkHU0yOjSAfbkeB3fWA8OgUfBixKvMlPKQ4OOSFbjC' #小嘍囉審核群
    #token = 'zhhw2k6lirJwSfpXhZH249cxodCafjozQdCtqUqpdXU' #小嘍囉管理版公告
    token = 'DSbKQs4mH5nTdEC0k3BGwNZiOUagMJiZGVTOcH4jMuh' #小嘍囉今日天氣
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type" : "application/x-www-form-urlencoded"}
        
    NowDate = datetime.now().strftime('%Y-%m-%d')
    print(NowDate)
    NowTime = NowDate + 'T06:00:00'
    
    Location_List = ['臺北市','新北市','桃園市','基隆市']
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
        weather =     json_format['records']['location'][0]['weatherElement'][0]['time'][0]    ['parameter']['parameterName']
        MinT =     json_format['records']['location'][0]['weatherElement'][2]['time'][0]    ['parameter']['parameterName']
        MaxT =     json_format['records']['location'][0]['weatherElement'][4]['time'][0]    ['parameter']['parameterName']
        pop =     json_format['records']['location'][0]['weatherElement'][1]['time'][0]    ['parameter']['parameterName']
        msg_weather = msg_weather + f'''
        
    {location}: {weather}
    氣溫: {MinT}度~{MaxT}度
    降雨機率: {pop}%'''
    
    payload = {'message': msg + msg_weather}

    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params =     payload)
    return r.status_code


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#加入群組自動發送
@handler.add(JoinEvent)
def handle_join(event):
    #message = TextSendMessage(text=" 安安你好\n還不知道晚餐要吃什麼好嗎?\n問我就對了！！\n\n輸入 晚餐吃啥 or 吃拉麵嗎\n來獲得良好的建議！\n-----\n懶得開google嗎?\n輸入：\n!想吃(空格)食物名\n我們幫你搜尋~\n-----\n若想再看一次此內容\n請輸入：\n!機器人自介")
    message = TextSendMessage(text=" 安安你好\n我只是個蒜頭，你問啥我就回答啥~\n輸入 \'請問蒜頭\'\n來獲得一些小建議\n-----\n若想再看一次此內容\n請輸入：\n!蒜頭自介")

    line_bot_api.reply_message(
            event.reply_token,message)
    print("JoinEvent =", JoinEvent)

# 加好友回覆
@handler.add(FollowEvent)
def handle_follow(event):
    #message = TextSendMessage(text=" 安安你好\n還不知道晚餐要吃什麼好嗎?\n問我就對了！！\n\n輸入 晚餐吃啥 or 吃拉麵嗎\n來獲得良好的建議！\n-----\n懶得開google嗎?\n輸入：\n!想吃(空格)食物名\n我們幫你搜尋~\n-----\n若想再看一次此內容\n請輸入：\n!機器人自介")
    message = TextSendMessage(text=" 安安你好\n我只是個蒜頭，你問啥我就回答啥~\n輸入 \'請問蒜頭\'\n來獲得一些小建議\n-----\n若想再看一次此內容\n請輸入：\n!蒜頭自介")

    line_bot_api.reply_message(
            event.reply_token,message)
    print("JoinEvent =", FollowEvent)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    strCheck = str(event.message.text)
    print(strCheck)
    
    #不接收line官方的訊息
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        
         #自我介紹同加入群組自動發送內容
 #        elif strCheck.find('晚餐機器人') >= 0:
#         elif strCheck == "!機器人自介" or strCheck == "！機器人自介":
        if strCheck == "!蒜頭自介" or strCheck == "！蒜頭自介":
 #            if strCheck.find('自我介紹') >= 0 :
            message = TextSendMessage(text=" 安安你好\n我只是個蒜頭，你問啥我就回答啥~\n輸入 \'請問蒜頭\'\n來獲得一些小建議\n-----\n若想再看一次此內容\n請輸入：\n!蒜頭自介")
            line_bot_api.reply_message(event.reply_token, message)

        #幹話
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

        #ChatGPT 回覆            
        elif strCheck.find('請問蒜頭') == 0:
            openai.api_key = chatGPT_key
            # 將第5個字元之後的訊息發送給 OpenAI
            prompt = strCheck[4:] 
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'user', 'content': prompt}
                ],
                temperature=1
            )
            # 接收到回覆訊息後，移除換行符號
            reply_msg = response['choices'][0]['message']['content'].replace('\n', '')

            message = TextSendMessage(text=reply_msg)
            line_bot_api.reply_message(event.reply_token, message)
        #開發者新增刪除
        elif event.message.text == "user_control":
            message = TextSendMessage(text=" useradd_ \n foodtype foodname \n useradd_reply\n foodtype replyfront replyend\n delete db-foodname ")
            line_bot_api.reply_message(event.reply_token, message)
        elif strCheck.find('useradd_') >= 0:    #新增
            reply = checkfoodlist.insert_record(event)
        elif strCheck.find('delete db') >= 0:   #刪除
            reply = checkfoodlist.line_delete_data(event)
            message = TextSendMessage(text= reply)
            line_bot_api.reply_message(event.reply_token, message)
        elif strCheck.find('！店家 ') == 0 or strCheck.find('!店家 ') == 0: #geocoding test
            reply = checkfoodlist.test_geocoding(event)
            message = TextSendMessage(text= reply)
            line_bot_api.reply_message(event.reply_token, message)
        elif strCheck.find('！氣象 ') == 0 or strCheck.find('!氣象 ') == 0: #geocoding test
            reply = checkfoodlist.lineNotifyWeather(event)
        elif strCheck.find('！公告 ') == 0 or strCheck.find('!公告 ') == 0: #geocoding test
            reply = checkfoodlist.lineNotifyAnnounce(event)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
