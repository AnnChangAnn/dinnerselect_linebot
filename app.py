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

#import os
#import psycopg2

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
    
#    print(body)
#        Udf831d201cfb768fdef117767f15f0a9
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    strCheck = str(event.message.text)
    print(strCheck)
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
    
    
        if event.message.text == "晚餐吃啥":
#            strfoodlist = "雞腿便當,咖哩飯,濃厚豚骨拉麵"
#            strfoodlist = "白湯拉麵 豚骨拉麵 泡菜拉麵 墨魚拉麵 海鮮蓋飯 鰻魚蓋飯 豬排蓋飯 天婦羅蓋飯 鱈魚蓋飯 海鮮蓋飯 中華蓋飯 生魚片蓋飯 什錦豆皮壽司 總匯三明治 鍋燒烏龍麵 韓式牛肉湯飯 銅鑼燒 泡芙 天婦羅蕎麥麵 蛋包飯 牛肉燴飯 茶泡飯 烤飯糰 照燒鰤魚 鹽烤鮭魚定食 烤竹莢魚定食 義式什錦湯 紅燒喜知次魚 海鮮炒飯 法式鹹派 蛋包飯 豬肉木耳炒蛋 海鮮義大利麵 蘑菇義大利麵 炸肉餅 炸竹筴魚 什錦煎餅 車輪餅 肉燥飯 紅燒金目鯛魚 燒烤西京味噌鰆魚 鯛姿蒸 蟹肉奶油可樂餅 牛肉蛋包飯 豬排咖哩飯 蟹肉燴炒飯 焢肉燴飯 烏龍麵 薑汁豬肉片 日式漢堡排 大阪壽司 山藥泥麥飯 燒肉井 美式肋排 中式油淋雞 香蒜牛排 蔥抓餅 泰式辣炒蝦 辣炒花蛤 辣炒花枝 辣炒豬 辣炒雞 泰味鳳梨蝦球 香茅辣炒雞肉 肉粽 泰式辣炒海鮮 酸辣叢林燒肉 醉仙牛肉 泰式生菜碎肉 鄉村牛肉 蟳蒸蛋 綜合壽司 關東煮 烤香魚 味噌湯 烤味噌魚 海鮮火鍋 和風沙拉 鮭魚飯團 蒜頭蛤湯 酸筍炒豬肉 炸蝦飯 豚天火燒 海老奶油燒 紅酒燉牛肉 干貝起士燒 牛肉奶油燒 牛蘆筍卷燒 鍋貼 鼎邊趖 泡泡冰 天婦羅 營養三明治 豆簽羹 蝦仁肉圓 鐵板燒 紅油抄手 大餅包小餅 刀削麵 豬肝湯 花枝羹 蚵仔煎 藥燉排骨 牛舌餅 新竹肉圓 貢丸 潤餅 蔥花煎餅 魷魚羹 米粉 潤餅 當歸鴨 蚵仔煎 炒花枝 肉羹 米糕 甜不辣 涼圓 大腸麵線 魷魚羹 魚酥羹 麻辣鴨血 麻辣臭豆腐 炸雞排 滷味 炒米粉 鴨肉羹 魯肉飯 排骨飯 煎餃 雞腿飯 臭豆腐 豪大大雞排 花枝羹 豬血糕 雞肉飯 藍藍路 維力雜醬麵 牛肉麵 鴨肉羹 御飯糰 MOS漢堡 肯德基 頂呱呱 丹丹 刺身 涮羊肉 廣東粥 麻辣鍋 雞絲麵 燒餅 油條 薑母鴨 甜不辣 水餃 可麗餅 小籠包 水餃 水煎包 車輪餅 蚵仔煎 炒米粉 炒羊肉 "
#            strfood = strfoodlist.split( )
#            message = TextSendMessage(text= random.choice(strfood))
#
#            #message = TextSendMessage(text=event.message.text)
#            line_bot_api.reply_message(event.reply_token, message)

            receivetxt = checkfoodlist.select_dinner_record(event)
            if receivetxt != "失敗了":
#                strreplylist = "吃,我想想... ,我想吃,要不要吃,我們去吃,走阿吃,欸嘿！吃,考慮一下,可吃,想吃,吃吃吃吃吃,晚餐吃起來！吃,吃一波,吃個,我覺得吃,今天就是要吃,當然是要吃"
#                strreply = strreplylist.split(",")
#            #            message = TextSendMessage(text= random.choice(strreply) + random.choice(strfood) + "!!")
#                message = TextSendMessage(text= random.choice(strreply) + receivetxt + "!!")
#                line_bot_api.reply_message(event.reply_token, message)
                
                message = TextSendMessage(text= receivetxt)
                line_bot_api.reply_message(event.reply_token, message)
            else:
                message = ""
                print(receivetxt)
                line_bot_api.reply_message(event.reply_token, message)
            
        elif event.message.text == "吃拉麵嗎":
            receivetxt = checkfoodlist.select_record(event)
#            print(receivetxt)
#            strfoodlist = "鬼金棒,壹之穴,豚人,麵屋輝,半熟堂,東京油組,Soba Shinn & 柑橘,美濃屋,勝王,你回來啦,吉天元,勝千代,涼風奄,小櫻,極匠,蘭丸,鷹流,悠然,麵屋壹慶,雞吉君,雞二,小川,真登,真劍,五之神,誠屋,道樂屋台,羽畠食堂,大和家,麵屋山茶,特濃屋,山嵐拉麵,武藤,旺味麵場,麵屋一燈,花月嵐,凪NAGI,一幻,麵屋武藏,麵屋一騎,小山拉麵,通堂,屯京拉麵,山頭火,霸嗎,双豚,森住康二,一番星,北一家,熊越岳,DUE ITALIAN,太陽番茄拉麵,玩笑亭,博多幸龍,初,一風堂,三冬麵鋪,沾麵玉,豚戈屋台,麵屋一鮫,隱家拉麵,荷麵亭,山形心心拉麵,百八龍拉麵,麵屋秋匠,墨洋拉麵,鳥人拉麵,麵屋武藏神山,一蘭,重熙老麵,麵屋千雲,TSUTA TAIWAN(蔦),三田製麵所,麵SATO SOBA,AJARI拉麵,札幌炎神,濟善老麵,哲麵,麵屋公子,辰拉麵,昕家,23私房拉麵,海貓亭,勝八,大角拉麵,極清拉麵,麵屋一擊,麵屋一虎,不二家拉麵"
#            strfood = strfoodlist.split(",")
#
            if receivetxt != "失敗了":
#                strreplylist = "好阿！吃,好！ ,我想吃,可以！吃,要不要吃,好！我們去吃,走阿吃,好好好好好！吃,好窩～那我們吃,可哇！吃,行！想吃,吃吃吃吃吃,拉麵吃起來！吃,吃一波"
#                strreply = strreplylist.split(",")
#    #            message = TextSendMessage(text= random.choice(strreply) + random.choice(strfood) + "!!")
#                message = TextSendMessage(text= random.choice(strreply) + receivetxt + "!!")
#                line_bot_api.reply_message(event.reply_token, message)
                message = TextSendMessage(text= receivetxt)
                line_bot_api.reply_message(event.reply_token, message)
            else:
                message = ""
                print(receivetxt)
                line_bot_api.reply_message(event.reply_token, message)
                
        elif event.message.text == "好美":
            message = TextSendMessage(text="哪有你美")
            line_bot_api.reply_message(event.reply_token, message)
        elif event.message.text == "中餐吃啥" or event.message.text == "午餐吃啥":
            message = TextSendMessage(text="沒有 只吃晚餐")
            line_bot_api.reply_message(event.reply_token, message)
        elif event.message.text == "早餐吃啥" or event.message.text == "早點吃啥":
            message = TextSendMessage(text="沒有 只吃晚餐")
            line_bot_api.reply_message(event.reply_token, message)
        elif event.message.text == "消夜吃啥" or event.message.text == "宵夜吃啥":
            message = TextSendMessage(text="沒有 只吃晚餐")
            line_bot_api.reply_message(event.reply_token, message)
        elif strCheck.find('晚餐吃啥') >= 0:
            if strCheck.find('自我介紹') >= 0 :
                message = TextSendMessage(text="輸入 晚餐吃啥 or 吃拉麵嗎 來獲得良好的建議！")
                line_bot_api.reply_message(event.reply_token, message)
        elif strCheck.find('吃') == 0:
            if strCheck.find('嗎') == len(strCheck) -1:
                if strCheck.find('晚餐') == -1 and strCheck.find('中餐') == -1 and strCheck.find('早餐') == -1 and strCheck.find('晚飯') == -1 and strCheck.find('午餐') == -1 and strCheck.find('早飯') == -1 and strCheck.find('宵夜') == -1 and strCheck.find('早點') == -1 and strCheck.find('消夜') == -1 and strCheck.find('夜消') == -1 and strCheck.find('夜宵') == -1:
                    message = TextSendMessage(text="不要！只吃拉麵！")
                    line_bot_api.reply_message(event.reply_token, message)
                elif strCheck.find('晚餐') >= 0 or strCheck.find('晚飯') >= 0:
                    message = TextSendMessage(text="好阿！要吃什麼？")
                    line_bot_api.reply_message(event.reply_token, message)
                else:
                    message = TextSendMessage(text="不要！只吃晚餐！")
                    line_bot_api.reply_message(event.reply_token, message)
        elif strCheck.find('我要新增拉麵') == 0 or strCheck.find('我要新增晚餐') == 0:
            reply = checkfoodlist.user_insert_record(event)
#            message = TextSendMessage(text= reply)
#            line_bot_api.reply_message(event.reply_token, message)
        elif strCheck.find('//管理者新增_') >= 0:
            reply = checkfoodlist.insert_record(event)
#            message = checkfoodlist.insert_record(event)
#            line_bot_api.reply_message(event.reply_token, message)
#        elif event.message.text == "create table":
#            reply = checkfoodlist.line_create_table(event)
        elif strCheck.find('管理者刪除db資料') >= 0:
            reply = checkfoodlist.line_delete_data(event)
            message = TextSendMessage(text= reply)
            line_bot_api.reply_message(event.reply_token, message)
        elif strCheck.find('test_program') >= 0:
            reply = checkfoodlist.line_test_program(event)
            message = TextSendMessage(text= reply)
            line_bot_api.reply_message(event.reply_token, message)
    #    else:
#        message = TextSendMessage(text="")
#        line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
