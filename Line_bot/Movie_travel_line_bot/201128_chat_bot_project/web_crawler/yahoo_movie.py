# 目標位置>>Yahoo>>電影>>Yahoo本週新片
# https://tw.movies.yahoo.com/movie_thisweek.html

import requests
import re
from bs4 import BeautifulSoup

# Yahoo電影
yahoo_movie_url = 'https://tw.movies.yahoo.com/movie_thisweek.html'  # 目標位置


def check_req_url(url):  # 測試請求網址是否請求成功
    resp = requests.get(url)  # 請求網址
    # print(resp.status_code) #錯誤時404,成功時200
    if resp.status_code != 200:  # 如果請求失敗
        print('Invalid url:', resp.url)  # 印出請求失敗的網址
        return "fail"  # 回傳失敗提示訊息
    else:
        return resp.text  # 回傳請求成功的html文字


def get_week_new_movies(webpage):  # 抓取電影資訊
    soup = BeautifulSoup(webpage, 'html.parser')  # 網頁解析
    movies = []  # 域設電影資訊存這裡

    # 抓取<div class="release_info_text"></div>內文字
    rows = soup.find_all('div', 'release_info_text')
    data_movie = dict()
    # print(rows)
    for row in rows:
        data_movie = dict()  # 存成{"key":"value"}格式
        # 電影名稱
        data_movie['ch_name'] = row.find('div', 'release_movie_name').a.text.strip()
        # 英文名稱
        data_movie['english_name'] = row.find('div', 'release_movie_name').find('div', 'en').a.text.strip()
        # 電影介紹
        data_movie['info'] = row.find('div', 'release_text').text.strip()
        # 期待度
        data_movie['expectation'] = row.find('div', 'leveltext').span.text.strip()
        # 上映日期 只抓日期 "上映日期：2020-11-20" -> match.group(0): "2020-11-20"
        data_movie['release_date'] = get_date(row.find('div', 'release_movie_time').text)

        movies.append(data_movie)  # 再被取代前先存入for 外面的movies=[]

    return movies


def get_date(date_str):
    # e.x. "上映日期：2017-03-23" -> match.group(0): "2020-11-20"
    # 記得import re
    # 1.\d找到數字
    # 2.要找一整組的所以\d+，+代表1個以上
    # 3.有可能有'-'

    pattern = '\d+-\d+-\d+'
    match = re.search(pattern, date_str)
    # print(match)
    # print(match.group(0))

    if match is None:
        return date_str
    else:
        return match.group(0)


if __name__ == '__main__':
    webpage = check_req_url(yahoo_movie_url)
    # print(webpage)

    if webpage:
        movies = get_week_new_movies(webpage)
        print(movies)

