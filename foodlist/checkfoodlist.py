#from __future__ import unicode_literals
import os

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, PostbackEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage
from bs4 import BeautifulSoup

import random
import re
import urllib
#import urllib2
import json

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
            (foodname, foodreply) = replyselect
            (url, url_google) = create_message_template(selecttype, foodname)
            print(url, url_google)
            return foodname, foodreply, url, url_google
        
#        print(reply)

    except:
        reply = "失敗了"
        return reply

def select_dinner_record(event):

    try:
#        record_list = formattext.prepare_record(event.message.text)
        selecttype = "food"
#        print(selecttype)
        foodreply = dbcontrol.line_select_overall(selecttype)
        (foodname, reply) = foodreply
        print(reply)

    except:
        reply = "失敗了"
    
    
    return reply

def google_text(event):

    try:
        foodname = event.message.text[4:]
        selecttype = "food"
        replyselect = dbcontrol.line_select_reply(selecttype)
        (reply_front, reply_end) = replyselect
        foodreply = reply_front + foodname + reply_end
        (url, url_google) = create_message_template(selecttype, foodname)
        print(url, url_google)
        return foodname, foodreply, url, url_google
        
#        print(reply)

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

def create_message_template(foodtype, txtmain):

    try:
        if foodtype == '拉麵':
            q_string = {'q': txtmain+ ' 拉麵'}
        else:
            q_string = {'q': txtmain }
            
        url = f"https://www.google.com/search?tbm=isch&tbs=isz:m&{urllib.parse.urlencode(q_string)}/"
        print(url)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
        
        soup = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=headers)),'html.parser')

#        req = urllib.request.Request(url, headers = headers)
#        conn = urllib.request.urlopen(req)

        print('fetch conn finish')

#        pattern = 'img data-src="\S*"'
#        pattern = 'data-iid="0" data-iurl="\S*"'
#        ]\n,["https://
#        pattern = ',["https://"\S*".jpg"'

        ActualImages=[]# contains the link for Large original images, type of  image
        for a in soup.find_all("img", class_="rg_i Q4LuWd tx8vtf", data-iid="0", limit=1):
            print(a.get('data-iurl'))
#            link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
#            ActualImages.append((link,Type))
            ActualImages.append(a.get('data-iurl'))
            print(ActualImages)

#        img_list = []
        
#        result_finditer = re.finditer(pattern, str(conn.read()))
#        print(type(result_finditer))
#        print(result_finditer)
#
##        for match in re.finditer(pattern, str(conn.read())):
#        for match in result_finditer:
#            img_list.append(match.group()[14:-1])
##            img_list.append(match.group()[3:-1])
#            print(img_list)

#        random_img_url = img_list[random.randint(0, len(img_list)+1)]
        random_img_url = ActualImages[random.randint(0, len(ActualImages)+1)]
        print('fetch img url finish')
        print(random_img_url)
        print(random_img_url)
        
        if foodtype == '拉麵':
            google_string = {'q': txtmain + ' 拉麵'}
        else:
            google_string = {'q': txtmain }
        print(google_string)
        
        url_google= f"https://www.google.com/search?{urllib.parse.urlencode(google_string)}"
        print(url_google)
        
        print(txtmain)

        return random_img_url, url_google

    except Exception as e:
        reply = "失敗了"
        print(e)
        return reply
       

