from pymongo import MongoClient


# 建立連線、連線至chat_bot_db  > user 資料表
client = MongoClient()
db = client.chat_bot_db
userDB = db.user



# 新增用戶資料
# 新增一個欄位 (經驗值)   # BUG 不得使用language欄位，不是唯一KEY
def add(x1,x2):
    for user_files in x1 :
        userDB.insert_one(user_files)
        db.user.update({'user_id': x2}, {'$set': {'level':round(0)}})
    return user_files


# 查詢用戶(經驗值) , 暫時回傳user_id
def find(x):
    data = userDB.find_one({'display_name':x})
    return data['level']



# 加經驗值 (目前為0.2)
def add_level(x):
    data = userDB.find_one({'display_name': x})
    data['level'] = data['level'] + 1
    db.user.update({'language': 'zh-Hant'}, {'$set': {'level':data['level']}})



#上傳票根 或 指定場景照片 ，依據級別 ，增加經驗值

