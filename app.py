# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('自己的Channel Access Token')
# 必須放上自己的Channel Secret
handler = WebhookHandler('自己的Channel Secret')

line_bot_api.push_message('你要推撥的user id', TextSendMessage(text='你可以開始了'))


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

 
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text

    emoji = [
    {
        "index": 0,
        "productId": "5ac1bfd5040ab15980c9b435",
        "emojiId": "001"
    },
    {
        "index": 2,
        "productId": "5ac1bfd5040ab15980c9b435",
        "emojiId": "002"
    },
    {
        "index": 15,
        "productId": "5ac1bfd5040ab15980c9b435",
        "emojiId": "002"
    }
    ]

    
    
    if re.match('拍照',message):
        flex_message = TextSendMessage(text='以下有雷，請小心',
        quick_reply=QuickReply(items=[
        QuickReplyButton(action=CameraAction(label="拍照")),
        QuickReplyButton(action=MessageAction(label="按我", text="按！")),
        QuickReplyButton(action=MessageAction(label="別按我", text="你按屁喔！爆炸了拉！！"))]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    if re.match('連結',message):
        text_message = TextSendMessage(text="連結 : https://cruelshare.com/")
        line_bot_api.reply_message(event.reply_token, text_message)
    if re.match('emoji',message):
        text_message = TextSendMessage(text='$ $ LINE emoji $', emojis=emoji)
        line_bot_api.reply_message(event.reply_token, text_message)
    
    """
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
    """

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
