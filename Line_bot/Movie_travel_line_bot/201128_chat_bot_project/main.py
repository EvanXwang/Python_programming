from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)
from rich_menu import link_user, unlink_user
import re
import requests
import json
from bs4 import BeautifulSoup
from opencc import OpenCC
from DB_files import DB
from linebot.models import RichMenu



app = Flask(__name__)
line_bot_api = LineBotApi('13850TvPyTes4LR2PzdYM08ibmKgplc924/r+wrRtMxAmKvstHzjZVa+f+WXOVXrdTZTp4xgUr6+VxcteBGalZS/JPmHoWNiLNPlRMjPVlN1fO5H8hX4zISfJ++LmQyWJLDdoRctH5SRKHOWQnXFagdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('df1ccae9be3c91365cfd806d9e2253b6')


# 監聽所有來自 /callback 的 Post Request
@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


 #用戶關注， 並取個資，存入本地端
from linebot.models import FollowEvent
@handler.add(FollowEvent)
def handle_follow_evant(event):
    users = []
    user_profile = line_bot_api.get_profile(event.source.user_id)
    users.append(vars(user_profile))
    # 用戶關注頻道後，自動綁定選單
    link_user(event.source.user_id)

    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name  # 使用者名稱
    url = profile.picture_url  # 使用者照片
    uid = profile.user_id  # 發訊者ID

    #  將用戶資訊存在檔案內
    # with open("users.txt", "a") as myfile:
    #     myfile.write(json.dumps(vars(user_profile), sort_keys=True))
    #     myfile.write('\n')
    #回傳個資
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage('Hello '+ user_profile.display_name+'，你不知道生活有多少荒謬，所謂黑色，是從真實和荒謬來的，電影也是如此，歡迎來到電影的世界 ， 對了，無聊的時候，可以點左下角的電癮咖，跟我聊天喔 :)')
    )
    DB.add(users,uid) #user 存入 資料庫


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = str(event.message.text).upper().strip()  # 使用者輸入的內容

    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name  # 使用者名稱
    url = profile.picture_url #使用者照片
    uid = profile.user_id  # 發訊者ID



#===============================================================
    if re.search("@", msg):
        result_message_array = []
        replyJsonPath = "material/"+event.message.text+"/reply.json"
        result_message_array = detect_json_array_to_new_message_array(replyJsonPath)
        line_bot_api.reply_message(event.reply_token,result_message_array)

    # elif re.match("解除", msg):  #內部測試用
    #     unlink_user(event.source.user_id)
    #
    # elif re.match("綁定", msg):  #內部測試用
    #     link_user(event.source.user_id)

    elif re.match("查詢", msg):  #查詢經驗值
        level = DB.find(user_name)
        line_bot_api.reply_message(event.reply_token, TextSendMessage('目前的經驗值為:'+ str(round(level))+'%'))

    elif re.match("加1", msg):  # 加經驗值
        DB.add_level(user_name)
        level = DB.find(user_name)
        line_bot_api.reply_message(event.reply_token, TextSendMessage('目前的經驗值為:'+ str(level)))

    elif(event.message.text.find('@') != 1):
        myuid = "Line"
        mymsg = event.message.text
        r1 = requests.get("http://api.brainshop.ai/get?bid=154159&key=8AUfCxCOwuyKOaCT",
                          headers={
                              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0"
                          },
                          params={
                              "uid": 154159,
                              "msg": mymsg
                          }
                          )
        r2 = json.loads(r1.text)
        cc = OpenCC("s2tw")
        # print(cc.convert(r2['cnt']))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=cc.convert(r2['cnt']))
        )


''' 
注意 json 外圍需加 []
未來要發消息給用戶，我們事先用json檔, 故要判斷json檔，轉換成合適的sendmessage
讀取指定的json檔案後，把json解析成不同格式的SendMessage讀取檔案，把內容轉換成json
將json轉換成消息, 放回array中，並把array傳出。
'''

# 引用會用到的套件
from linebot.models import (
    ImagemapSendMessage, TextSendMessage, ImageSendMessage, LocationSendMessage, FlexSendMessage, VideoSendMessage , StickerSendMessage , AudioSendMessage
)

import json
from linebot.models.template import (
    ButtonsTemplate, CarouselTemplate, ConfirmTemplate, ImageCarouselTemplate
)

from linebot.models.template import *
def detect_json_array_to_new_message_array(fileName):
    # 開啟檔案，轉成json
    with open(fileName,encoding='utf8') as f:
        jsonArray = json.load(f)

    # 解析json
    returnArray = []
    for jsonObject in jsonArray:

        # 讀取其用來判斷的元件
        message_type = jsonObject.get('type')

        # 轉換
        if message_type == 'text':
            returnArray.append(TextSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'imagemap':
            returnArray.append(ImagemapSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'template':
            returnArray.append(TemplateSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'image':
            returnArray.append(ImageSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'sticker':
            returnArray.append(StickerSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'audio':
            returnArray.append(AudioSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'location':
            returnArray.append(LocationSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'flex':
            returnArray.append(FlexSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'video':
            returnArray.append(VideoSendMessage.new_from_json_dict(jsonObject))

            # 回傳
    return returnArray


# ============ QuickReplay =================
'''
當收到PostbackEvent時
告知handler
'''
from linebot.models import PostbackEvent
from linebot.models import (
    QuickReply,
    QuickReplyButton,
    MessageAction
)
@handler.add (PostbackEvent)
def handel_postback_event(event):
    postback_data = event.postback.data
    '''
    製作QuickReply
    先做按鍵
    再作QuickReply
    夾帶SendMessae內，送回給用戶
    '''
    qrb1 = QuickReplyButton(action=MessageAction(label='台南鹽水教堂',text='@尋寶'))
    qrb2 = QuickReplyButton(action=MessageAction(label='高雄老瓊泡沫紅茶店', text='@尋寶1'))

    type1 = QuickReplyButton(action=MessageAction(label='動作', text='@動作'))
    type2 = QuickReplyButton(action=MessageAction(label='恐怖', text='@恐怖'))
    type3 = QuickReplyButton(action=MessageAction(label='浪漫愛情', text='@浪漫愛情'))
    type4 = QuickReplyButton(action=MessageAction(label='科幻', text='@科幻'))
    type5 = QuickReplyButton(action=MessageAction(label='喜劇', text='@喜劇'))
    type6 = QuickReplyButton(action=MessageAction(label='劇情', text='@劇情'))

    movie1 = QuickReplyButton(action=MessageAction(label='本週新片', text='本週新片'))
    movie2 = QuickReplyButton(action=MessageAction(label='上映中', text='上映中'))
    movie3 = QuickReplyButton(action=MessageAction(label='即將上映', text='即將上映'))
    movie4 = QuickReplyButton(action=MessageAction(label='預告片', text='預告片'))
    movie5 = QuickReplyButton(action=MessageAction(label='排行榜', text='排行榜'))
    movie6 = QuickReplyButton(action=MessageAction(label='電影新聞', text='電影新聞'))
    movie7 = QuickReplyButton(action=MessageAction(label='影評', text='影評'))

    quick_reply_list = QuickReply([qrb1, qrb2])
    quick_reply_movie_list = QuickReply([type1, type2, type3, type4, type5, type6])
    quick_reply_movie_news = QuickReply([movie1, movie2, movie3, movie4, movie5, movie6, movie7])

    if postback_data == 'data1':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage('想重溫那個電影場景呢??',quick_reply=quick_reply_list)
        )

    elif postback_data == 'data2':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage('請選擇電影類型',quick_reply=quick_reply_movie_list)
        )
    elif postback_data == 'data3':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage('請選擇',quick_reply=quick_reply_movie_news)
        )

'''
解壓縮模型
'''
'''
from zipfile import ZipFile
with ZipFile('converted_savedmodel.zip', 'r') as zipObj:
   # Extract all the contents of zip file in different directory
   zipObj.extractall('converted_savedmodel')
'''

'''
載入類別列表
'''
class_dict = {}
with open('converted_savedmodel/labels.txt') as f:
    for line in f:
       (key, val) = line.split()
       class_dict[int(key)] = val
'''

圖片消息，解析圖片

'''

import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

# 引用套件
from linebot.models import (
    MessageEvent, ImageMessage, TextSendMessage
)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = tensorflow.keras.models.load_model('converted_savedmodel/model.savedmodel')

import time

@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name  # 使用者名稱
    print(time.asctime(time.localtime(time.time())))
    message_content = line_bot_api.get_message_content(event.message.id)
    file_name = event.message.id + '.jpg'
    with open('images/'+file_name, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    print(time.asctime(time.localtime(time.time())))

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open('images/'+file_name)

    # resize the image to a 224x224 with the same strategy as in TM2:
    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    print(time.asctime(time.localtime(time.time())))

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # display the resized image
    #image.show()

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0 - 1)

    # Load the image into the array
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array[0:224, 0:224, 0:3]

    # run the inference
    prediction = model.predict(data)
    print(time.asctime(time.localtime(time.time())))
    max_probability_item_index = np.argmax(prediction[0])

    msg1 = '月球，即地衛一，俗稱月亮或月，古稱太陰、玄兔，是地球唯一的天然衛星，並且是太陽系中第五大的衛星'
    msg2 = '你能一口氣唸出來嗎??四十四里外的石獅寺，有四十四隻石獅子，這四十四隻石獅子旁，有四十四棵柿子樹，石老頭吃了澀柿子，躺在石獅子旁捉蝨子。'
    msg3 = '做人要像一支蠟燭，燃燒自己卻在黑暗中照亮別人'
    msg4 = '據說紅茶佔了世界茶業銷量的75%'
    msg5 = '今天的撲克牌設計有五十二張正牌，是因為一年有五十二個星期'
    msg6 = 'Bravo! 提升經驗值!!!\n\n'

    if prediction.max() > 0.8:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(msg6 + '%s' % (class_dict.get(max_probability_item_index))))
        if class_dict.get(max_probability_item_index) == msg1 or msg2 or msg3 or msg4 or msg5: # 取出value值
           DB.add_level(user_name)# 升級

    else:

        line_bot_api.reply_message(event.reply_token,TextSendMessage("猜錯囉, 人生就差這一步! "))

if __name__ == "__main__":
    app.run()



