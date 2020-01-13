#from __future__ import unicode_literals
import os

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, PostbackEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage

import random

# 我們的函數
from foodlist import dbcontrol, formattext

# Channel Access Token
line_bot_api = LineBotApi('OxFz4p5BSnf4OMX3gG5RsWOoDt1xKqb/MgIgkPpCFZAG97cU085VHbKqX3M7PxMT7UcMqPLD1g2/GAtXLrCtA3csBzCLulogW6zckNvfTl1UDo8ypLml38KT8kWLtPeE53AkumUg+w+MYlTD3Cp/sgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
#handler = WebhookHandler('4c1f11afcd419b717773c2ccab3ff01c')

# 請 LINE 幫我們存入資料
def insert_record(event):
    
    try:
        if event.message.text.find('//管理者新增_回應') >= 0:
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

def select_record(event):

    try:
#        record_list = formattext.prepare_record(event.message.text)
        selecttype = event.message.text[1:3]
        print(selecttype)
        reply = dbcontrol.line_select_overall(selecttype)
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



