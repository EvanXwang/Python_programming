from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('6PNMWNgLyfypWgLK4cF8n8ztXBSRNWtrDL+OwD49FjHy4zJUfFFQp6AHl/iO1s8g4Q5k4Ad7qWxvp+aqTipdy452y4lclHBTLu+waoUyxD+LILzxeFF1WOe9TOI8YFTYHkiw5GSng6ynOtOm+DfnuAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('63922ce4140d7be4844b7c7f01bbc795')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
