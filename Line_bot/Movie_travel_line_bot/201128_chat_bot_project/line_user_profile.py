demo_message_json_string='''
{
  "type": "text",
  "text": "您好！"
}
'''
import json
demo_message_json = json.loads(demo_message_json_string)
from linebot.models import *
text_send_message = TextSendMessage.new_from_json_dict(demo_message_json)


from linebot.models import ( MessageEvent ,TextMessage)
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
  line_bot_api.reply_message(
      event.reply_token,
      text_send_message
      )