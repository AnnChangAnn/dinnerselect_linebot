#from __future__ import unicode_literals
import os

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, PostbackEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage
from bs4 import BeautifulSoup
#from selenium import webdriver

import random
import re
import urllib
#import urllib2
import json

# 我們的函數
from foodlist import dbcontrol, formattext
import requests

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
#        soup = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=headers)),'lxml')

#        req = urllib.request.Request(url, headers = headers)
#        conn = urllib.request.urlopen(req)

        print('fetch conn finish')
#        print(soup)

#        pattern = 'img data-src="\S*"'
#        pattern = 'data-iid="0" data-iurl="\S*"'
#        ]\n,["https://
#        pattern = ',["https://"\S*".jpg"'

        ActualImages=[]# contains the link for Large original images, type of  image
        for a in soup.find_all("img", class_="rg_i Q4LuWd tx8vtf", limit=1):
            print(a.get('data-iurl'))
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
#        random_img_url = ActualImages[random.randint(0, len(ActualImages)+1)]
        random_img_url = ActualImages[0]
        print('fetch img url finish')
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
 
def test_geocoding(event):

    try:
     
        txttext = event.message.text
        text_list = txttext.split(' ')
        q_string = text_list[1]
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={q_string}&language=zh-TW&key=AIzaSyDK-Gv6pcSDFWyexGbFGNVRuerH8HsNWQU"
        print(url)

        req = requests.get(url)
        print('request success!!')
        req_dict = req.json()
        json_string = json.dumps(req_dict)
        json_format = json.loads(json_string)
        lat = json_format['results'][0]['geometry']['location']['lat']
        lng = json_format['results'][0]['geometry']['location']['lng']
        loc = json_format['results'][0]['formatted_address']
        print(lat, lng)
        output = (f"""經度:{lng}\n"""
                  f"""緯度:{lat}\n"""
                  f"""地址:{loc}""")
        print(output)
        
        return output
     
    
    except:
        reply = "查無此地點"
        return reply

def lineNotifyWeather(event):
    
    try:
        txttext = event.message.text
        #text_list = txttext.split(' ')
        #q_string = text_list[1]
        q_string = txttext[4:]
        
        #msg = '嗨嗨'
        #token = 'C2MMtPLrfSbUaTyaGWxZM7Zq58LwRKKoNjMfMWXtpGt' #國泰發行權杖
        token = 'Q2bIg5ezRJOwgRm6pk6kSQeaKXw82OoPg2XzaTWPnwp' #cathaybk測試權杖
        #token = 'USkHU0yOjSAfbkeB3fWA8OgUfBixKvMlPKQ4OOSFbjC' #小嘍囉審核群
        #token = 'zhhw2k6lirJwSfpXhZH249cxodCafjozQdCtqUqpdXU' #小嘍囉管理版公告
        
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type" : "application/x-www-form-urlencoded"}
            
        Location_List = ['臺北市','新北市','桃園市','基隆市']
        msg = "\r    時間：6:00~18:00\r"
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
            feeling =     json_format['records']['location'][0]['weatherElement'][3]['time'][0]    ['parameter']['parameterName']
            MinT =     json_format['records']['location'][0]['weatherElement'][2]['time'][0]    ['parameter']['parameterName']
            MaxT =     json_format['records']['location'][0]['weatherElement'][4]['time'][0]    ['parameter']['parameterName']
            pop =     json_format['records']['location'][0]['weatherElement'][1]['time'][0]    ['parameter']['parameterName']
            #lng = json_format['results'][0]['geometry']['location']['lng']
            #print(lat)
            #print(lat, lng)
            msg_weather = msg_weather + f'''
            
    {location}
    {weather}，{feeling}
    氣溫: {MinT}度~{MaxT}度
    降雨機率: {pop}%'''
        
        payload = {'message': msg + msg_weather}
            
            
        #payload = {'message': q_string}
        r = requests.post("https://notify-api.line.me/api/notify", headers = headers,     params =     payload)
        return q_string
        
    except:
        reply = "failed"
        return reply

def lineNotifyAnnounce(event):

    try:
        txttext = event.message.text
        #text_list = txttext.split(' ')
        #q_string = text_list[1]
        q_string = txttext[4:]
    
        #msg = '嗨嗨'
        #token = 'C2MMtPLrfSbUaTyaGWxZM7Zq58LwRKKoNjMfMWXtpGt' #國泰發行權杖
        #token = 'Q2bIg5ezRJOwgRm6pk6kSQeaKXw82OoPg2XzaTWPnwp' #cathaybk測試權杖
        #token = 'USkHU0yOjSAfbkeB3fWA8OgUfBixKvMlPKQ4OOSFbjC' #小嘍囉審核群
        #token = 'zhhw2k6lirJwSfpXhZH249cxodCafjozQdCtqUqpdXU' #小嘍囉管理版公告
        token = 'mT4u7fjyHcfQLjpj2e1JnZrajS8Cz9wweBfD0Ad85nb' #小嘍囉公告
    
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type" : "application/x-www-form-urlencoded"}
    
        payload = {'message': q_string}
        r = requests.post("https://notify-api.line.me/api/notify", headers = headers,         params =     payload)
        return q_string
    
    except:
        reply = "failed"
        return reply
        
    #return reply
