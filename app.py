from flask import Flask, request, abort

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

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('OxFz4p5BSnf4OMX3gG5RsWOoDt1xKqb/MgIgkPpCFZAG97cU085VHbKqX3M7PxMT7UcMqPLD1g2/GAtXLrCtA3csBzCLulogW6zckNvfTl1UDo8ypLml38KT8kWLtPeE53AkumUg+w+MYlTD3Cp/sgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('4c1f11afcd419b717773c2ccab3ff01c')

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
    message = TextSendMessage(text=" 各位安安\n還不知道晚餐要吃什麼好嗎\n問我就對了！！\n\n輸入 晚餐吃啥 or 吃拉麵嗎\n來獲得良好的建議！\n-----\n想新加入菜單\n請輸入：\n\n我要新增拉麵(空格)拉麵名\n\n或\n\n我要新增晚餐(空格)食物名\n\n來加入菜單\n例如：\n我要新增晚餐 蛋炒飯\n\n我們就會幫您加入'蛋炒飯'這個菜單\n-----\n若想再看一次此內容\n請輸入：\n晚餐機器人自我介紹")

    line_bot_api.reply_message(
            event.reply_token,message)
    print("JoinEvent =", JoinEvent)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    strCheck = str(event.message.text)
    print(strCheck)
    
    #不接收line官方的訊息
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        
        #晚餐特定回覆
        if event.message.text == "晚餐吃啥":
            #查詢晚餐資料庫
            receivetxt = checkfoodlist.select_dinner_record(event)
            #成功則回覆內容ㄝ，失敗則不回話
            if receivetxt != "失敗了":
                message = TextSendMessage(text= receivetxt)
                line_bot_api.reply_message(event.reply_token, message)
            else:
                message = ""
                print(receivetxt)
                line_bot_api.reply_message(event.reply_token, message)
        
        #拉麵特定回覆
        elif event.message.text == "吃拉麵嗎":
            #查詢晚餐資料庫
            receivetxt = checkfoodlist.select_record(event)
            #成功則回覆內容ㄝ，失敗則不回話
            if receivetxt != "失敗了":
                message = TextSendMessage(text= receivetxt)
                line_bot_api.reply_message(event.reply_token, message)
            else:
                message = ""
                print(receivetxt)
                line_bot_api.reply_message(event.reply_token, message)
        
        #幹話
        elif event.message.text == "好美":
            message = TextSendMessage(text="哪有你美")
            line_bot_api.reply_message(event.reply_token, message)
        
        #一律只吃晚餐
        elif event.message.text == "中餐吃啥" or event.message.text == "午餐吃啥" or event.message.text == "早餐吃啥" or event.message.text == "早點吃啥" or event.message.text == "消夜吃啥" or event.message.text == "宵夜吃啥":
            message = TextSendMessage(text="沒有 只吃晚餐")
            line_bot_api.reply_message(event.reply_token, message)
#        elif event.message.text == "早餐吃啥" or event.message.text == "早點吃啥":
#            message = TextSendMessage(text="沒有 只吃晚餐")
#            line_bot_api.reply_message(event.reply_token, message)
#        elif event.message.text == "消夜吃啥" or event.message.text == "宵夜吃啥":
#            message = TextSendMessage(text="沒有 只吃晚餐")
#            line_bot_api.reply_message(event.reply_token, message)

        #自我介紹同加入群組自動發送內容
        elif strCheck.find('晚餐機器人') >= 0:
            if strCheck.find('自我介紹') >= 0 :
                message = TextSendMessage(text="各位安安\n還不知道晚餐要吃什麼好嗎\n問我就對了！！\n\n輸入 晚餐吃啥 or 吃拉麵嗎\n來獲得良好的建議！\n-----\n想新加入菜單\n請輸入：\n\n我要新增拉麵(空格)拉麵名\n\n或\n\n我要新增晚餐(空格)食物名\n\n來加入菜單\n例如：\n我要新增晚餐 蛋炒飯\n\n我們就會幫您加入'蛋炒飯'這個菜單\n-----\n若想再看一次此內容\n請輸入：\n晚餐機器人自我介紹")
                line_bot_api.reply_message(event.reply_token, message)
                
        #"吃??嗎"的特定回覆
        elif strCheck.find('吃') == 0:
            if strCheck.find('嗎') == len(strCheck) -1:
                #火鍋特定回覆
                if strCheck.find('火鍋') >= 0:
                    receivetxt = checkfoodlist.select_record(event)
                    if receivetxt != "失敗了":
                        message = TextSendMessage(text= receivetxt)
                        line_bot_api.reply_message(event.reply_token, message)
                    else:
                        message = ""
                        print(receivetxt)
                        line_bot_api.reply_message(event.reply_token, message)
                elif strCheck.find('晚餐') == -1 and strCheck.find('中餐') == -1 and strCheck.find('早餐') == -1 and strCheck.find('晚飯') == -1 and strCheck.find('午餐') == -1 and strCheck.find('早飯') == -1 and strCheck.find('宵夜') == -1 and strCheck.find('早點') == -1 and strCheck.find('消夜') == -1 and strCheck.find('夜消') == -1 and strCheck.find('夜宵') == -1:
                    message = TextSendMessage(text="不要！只吃拉麵！")
                    line_bot_api.reply_message(event.reply_token, message)
                elif strCheck.find('晚餐') >= 0 or strCheck.find('晚飯') >= 0:
                    message = TextSendMessage(text="好阿！要吃什麼？")
                    line_bot_api.reply_message(event.reply_token, message)
                else:
                    message = TextSendMessage(text="不要！只吃晚餐！")
                    line_bot_api.reply_message(event.reply_token, message)
        
        #使用者新增
        elif strCheck.find('我要新增拉麵') == 0 or strCheck.find('我要新增晚餐') == 0:
            reply = checkfoodlist.user_insert_record(event)
            
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
        elif strCheck.find('test_program') >= 0:    #測試 目前無用
#            reply = checkfoodlist.line_test_program(event)
#            message = TextSendMessage(text= reply)
#            line_bot_api.reply_message(event.reply_token, message)
#            try:
             strCheck = strCheck[14:]
             print(strCheck)
             q_string = {'tbm': 'isch', 'tbs': 'isz:m', 'q': strCheck}
             url = f"https://www.google.com/search?{urllib.parse.urlencode(q_string)}/"
             print(url)
             headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

             req = urllib.request.Request(url, headers = headers)
             conn = urllib.request.urlopen(req)

             print('fetch conn finish')

             pattern = 'img data-src="\S*"'
             img_list = []

             for match in re.finditer(pattern, str(conn.read())):
                 img_list.append(match.group()[14:-1])
#                 print(img_list)

#             random_img_url = img_list[random.randint(0, len(img_list)+1)]
             random_img_url = img_list[-1]
             print('fetch img url finish')
             print(random_img_url)
             
             line_bot_api.reply_message(
                 event.reply_token,
                 ImagemapSendMessage(
                     base_url=random_img_url,
                     alt_text='test',
                     base_size=BaseSize(height=1040, width=1040),
                     actions=[
                         URIImagemapAction(
                             label = "hello",
                             link_uri=random_img_url,
                             area=ImagemapArea(
                                 x=0, y=0, width=1040, height=1040
                             )
                         ) #,
#                         MessageImagemapAction(
#                             text='hello',
#                             area=ImagemapArea(
#                                 x=0, y=0, width=520, height=1040
#                             )
#                         )
                     ]
                 )
             )
            # 如果找不到圖，就學你說話
#            except:
#                line_bot_api.reply_message(
#                    event.reply_token,
#                    TextSendMessage(text=event.message.text)
#                )
#                pass

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
