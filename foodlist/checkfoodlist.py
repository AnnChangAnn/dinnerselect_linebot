#from __future__ import unicode_literals
import os

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, PostbackEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage

import random
import re
import urllib

# 我們的函數
from foodlist import dbcontrol, formattext

# Channel Access Token
line_bot_api = LineBotApi('OxFz4p5BSnf4OMX3gG5RsWOoDt1xKqb/MgIgkPpCFZAG97cU085VHbKqX3M7PxMT7UcMqPLD1g2/GAtXLrCtA3csBzCLulogW6zckNvfTl1UDo8ypLml38KT8kWLtPeE53AkumUg+w+MYlTD3Cp/sgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
#handler = WebhookHandler('4c1f11afcd419b717773c2ccab3ff01c')

# 請 LINE 幫我們存入資料
def insert_record(event):
    
    try:
        if event.message.text.find('useradd_reply') >= 0:
            record_list = formattext.prepare_reply(event.message.text)
            reply = dbcontrol.line_insert_reply(record_list)
        else:
            record_list = formattext.prepare_record(event.message.text)
            reply = dbcontrol.line_insert_record(record_list)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )

    except:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='失敗了')
        )

    return True

def user_insert_record(event):

    try:
#        print(event.message.text)
        if event.message.text.find('拉麵') >= 0:
#            print(event.message.text.find('拉麵'))
            record_list = [('拉麵', event.message.text[7:])]
#            print(record_list)
#            reply = "test"
            reply = dbcontrol.user_insert_record(record_list)
        elif event.message.text.find('晚餐') >= 0:
#            print(event.message.text.find('晚餐'))
            record_list = [('food', event.message.text[7:])]
#            print(record_list)
#            reply = "test"
            reply = dbcontrol.user_insert_record(record_list)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )

    except:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='失敗了')
        )

    return True

def select_record(event):

    try:
#        record_list = formattext.prepare_record(event.message.text)
        if event.message.text.find('火鍋') >= 0:
            selecttype = "火鍋sp"
            print(selecttype)
            reply = dbcontrol.line_select_sp(selecttype)
        else:
            selecttype = event.message.text[1:3]
            print(selecttype)
            replyselect = dbcontrol.line_select_overall(selecttype)
            reply = create_message_template(selecttype, replyselect)
            
        
        print(reply)

    except:
        reply = "失敗了"
       
       
    return reply

def select_dinner_record(event):

    try:
#        record_list = formattext.prepare_record(event.message.text)
        selecttype = "food"
#        print(selecttype)
        reply = dbcontrol.line_select_overall(selecttype)
        print(reply)

    except:
        reply = "失敗了"
    
    
    return reply

def line_create_table(event):

    try:
        reply = dbcontrol.line_create_table(event.message.text)
        print(reply)

    except:
        reply = "失敗了"

    return reply

def line_delete_data(event):

    try:
        deletefood = event.message.text[10:]
        print(deletefood)
        reply = dbcontrol.line_delete_record(deletefood)
        print(reply)

    except:
        reply = "失敗了"
    
    return reply

def line_test_program(event):

    try:
        txttext = event.message.text
        print(txttext)
        reply = dbcontrol.line_test_program(txttext)
        print(reply)

    except:
        reply = "失敗了"

    return reply

def create_message_template(txtmain, txtreply):

    try:
        q_string = {'q': txtmain}
        url = f"https://www.google.com/search?tbm=isch&tbs=isz:m&{urllib.parse.urlencode(q_string)}/"
        print(url)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

        req = urllib.request.Request(url, headers = headers)
        conn = urllib.request.urlopen(req)

        print('fetch conn finish')

        pattern = 'img data-src="\S*"'
        img_list = []
        
       # result_finditer = re.finditer(pattern, str(conn.read()))
       # print(type(result_finditer))
       # print(result_finditer)
        
        for match in re.finditer(pattern, str(conn.read())):
       # for match in result_finditer:
            img_list.append(match.group()[14:-1])

        random_img_url = img_list[random.randint(0, len(img_list)+1)]
        print('fetch img url finish')
        print(random_img_url)
        
        google_string = {'q': txtmain + '+拉麵'}
        url_google= f"https://www.google.com/search?{urllib.parse.urlencode(google_string)}"
        print(url_google)
        
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text=str(txtreply),
                template=ButtonsTemplate(
                    thumbnail_image_url=random_img_url,
                    title=txtmain,
                    text=str(txtreply),
                    actions=[
                        URIAction(
                            label='Google ' + txtmain,
                            uri=url_google
                        )
                    ]
                )
            )
        )
        reply = "success"
        print(reply)
         

    except:
        reply = "失敗了"
       
       
    return reply

