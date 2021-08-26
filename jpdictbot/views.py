from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage

import os
import random
import requests
from bs4 import BeautifulSoup
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

DICT_URL = 'https://dict.asia/jc/'
IMG_URLS = [
    'https://truth.bahamut.com.tw/s01/202107/17af8617140115fad32bc3d9fa38a5b1.JPG',
    'https://truth.bahamut.com.tw/s01/202104/986476ed90ac924402c120edaf57d2fe.JPG',
    'https://truth.bahamut.com.tw/s01/201911/4e3eb1c83a9c6204fd1cdcff2206e831.JPG',
    'https://truth.bahamut.com.tw/s01/202002/4f926ddf0697131d0220bd79ea5380d8.JPG',
    'https://truth.bahamut.com.tw/s01/202003/35b393440a4f53666fb07107e6df896f.JPG',
    'https://truth.bahamut.com.tw/s01/202004/1cecf7904f5ac8408c555f4ffad83d68.JPG',
    'https://truth.bahamut.com.tw/s01/201902/df15787a89f2db08eaca4d30bda6d707.JPG',
    'https://truth.bahamut.com.tw/s01/202005/a6eba2a6e38379a66407b2157f889481.JPG',
    'https://truth.bahamut.com.tw/s01/202104/0dd16ab9be7200d0c89e5b0fd87bf271.JPG',
    'https://truth.bahamut.com.tw/s01/202104/a8fa7c731223d7c69b5d96b3651ed6ef.JPG',
    'https://truth.bahamut.com.tw/s01/202104/bc19066fd897acc63d9a4ee3bcb27ea6.JPG',
    'https://truth.bahamut.com.tw/s01/202104/17dfe53f6335fb2f7f0d7ced423cf507.JPG',
    'https://truth.bahamut.com.tw/s01/202104/7cb811ed4a33a7edbee697a827953b04.JPG',
]
 
@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                ret = crawlDictionary(event.message.text)
                if ret != '':
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text=ret)
                    )
                else:
                    img = random.choice(IMG_URLS)
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        ImageSendMessage(
                            original_content_url=img,
                            preview_image_url=img
                        )
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def crawlDictionary(word):
    ret = ''
    print(DICT_URL + word)
    r = requests.get(DICT_URL + word)
    bs = BeautifulSoup(r.text, 'html.parser')
    for section in bs.find_all('div', attrs={'id': 'jp_comment'}):
        if (section != None):
            ret += section.find('span', attrs={'class': 'trs_jp bold'}).text
            comment = section.find('span', attrs={'id': 'comment_0'})
            for t in comment.find_all(text=True):
                if (t == '　 '):
                    ret += '     '
                elif (t != '\n'):
                    ret += t + '\n'
    return ret
