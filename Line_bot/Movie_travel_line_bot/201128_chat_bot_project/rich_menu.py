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
#創造line_boot_api

line_bot_api = LineBotApi('13850TvPyTes4LR2PzdYM08ibmKgplc924/r+wrRtMxAmKvstHzjZVa+f+WXOVXrdTZTp4xgUr6+VxcteBGalZS/JPmHoWNiLNPlRMjPVlN1fO5H8hX4zISfJ++LmQyWJLDdoRctH5SRKHOWQnXFagdB04t89/1O/w1cDnyilFU=')

# 將設定檔傳給line
# 讀取json檔
# 轉成json格式
# 注意!!! MENU JSON檔  最外面不用加 []  , 否則會讀不出來 (跟 material的json 不一樣)
import json
from linebot.models import RichMenu

def open_menu_json():
    # #開啟  圖文選單的json檔 並存成 rich_menu_json_object
    with open('movie_menu_1.json', 'r', encoding='utf8') as json_file:
        rich_menu_json_object = json.load(json_file)

    # 將json格式做成RichMenu的變數
    rich_menu_config = RichMenu.new_from_json_dict(rich_menu_json_object)

    # line_bot_api傳給line
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu_config)

    # 把rich_menu_id打印出來
    return rich_menu_id


def load_menu(menu_id):
    # 把照片傳給指定的圖文選單ID
    # 準備圖片
    # 把圖片載入
    # 命令line_bot_api 將圖片上傳到指定圖文選單的id上
    rich_menu_id = menu_id
    with open('Movie_menu_5.png', 'rb') as  image_file:
        line_bot_api.set_rich_menu_image(
            rich_menu_id=rich_menu_id,
            content_type='image/jpeg',
            content=image_file
        )

def link_user(userid):
    #綁定用戶與圖文選單
    rich_menu_id = 'richmenu-1c88f1fafd0998bb9199323f32742da6'
    line_bot_api.link_rich_menu_to_user(
        user_id= userid,
        rich_menu_id=rich_menu_id
    )

def unlink_user(userid):
    #解除綁定
    line_bot_api.unlink_rich_menu_from_user(
        user_id= userid
    )

def del_menu(menu_id):
    #刪除圖文選單
    rich_menu_id = menu_id
    line_bot_api.delete_rich_menu(rich_menu_id=rich_menu_id)


#
# # #creat 圖文選單 - 開啟選單json檔，並創建rich_menu_id
# menu_id = open_menu_json()
# #
# # #set 圖文選單 - 照片傳給指定的圖文選單ID
# load_menu(menu_id)


#link 用戶
# link_user(menu_id)



#解除關係
# unlink_user()
# del_menu()



# 刪除全部的選單
# rich_menu_list = line_bot_api.get_rich_menu_list()
# for rich_menu in rich_menu_list:
#     del_menu(rich_menu.rich_menu_id)



#列出全部menu id list
# rich_menu_list = line_bot_api.get_rich_menu_list()
# for rich_menu in rich_menu_list:
#     print(rich_menu.rich_menu_id)