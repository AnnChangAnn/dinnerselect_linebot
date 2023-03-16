import openai
import os
from flask import Flask, request, abort, render_template

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from foodlist import checkfoodlist


app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN',  None))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET',  None))
chatGPT_key = os.getenv('AI_APIKEY', None)

# 喚醒heroku
@app.route("/")
def home():
    return render_template("home.html")

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'



@handler.add(MessageEvent, message=TextMessage)
async def handle_message(event):
    strCheck = str(event.message.text)
    print(strCheck)

    # 不接收line官方的訊息
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        if strCheck == "!機器人自介" or strCheck == "！機器人自介":
         #            if strCheck.find('自我介紹') >= 0 :
            message = TextSendMessage(text=" 安安你好\n請輸入：\n!機器人自介")
            await line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
