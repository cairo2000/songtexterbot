# coding=utf-8
from telebot import types
import telebot
import time
import requests
#import win32api
#from aiogram.dispatcher import Dispatcher

from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

'''
#===========================================================================================================================================4
l = 'группа крови'.replace(' ', '+')
way = []
topway = []
name = []
topname = []
text = []




'''

op_showtext=1
op_next=2
op_top20=3
op_yandexmusic=4

short = 'https://clck.ru/--?url='

max_songs_count_perpage=5
btn_marker="btn" 
siteurl = 'https://alloflyrics.cc'

def link_shorter(link):
    shortlink = requests.get(short+link).text
    return shortlink
'''
>>> url = 'http://bit.ly'
>>> import urllib2
>>> fetcher = urllib2.urlopen(
      'https://clck.ru/--?url='+
      url)
>>> fetcher.read()
'https://clck.ru/8JM'
'''

#==========================================================================
def searchSongsShowButtons(msg_chat_id, url, startindex):
    lastSearchIndex=0
    #составляем поисковый url
    #search_text = msg_text.replace(' ', '+')
    #url = siteurl+'search/?s='+search_text
    #bot.send_message(msg_chat_id, "url=[{}]".format(url))
    #print(url)
    #отправляем запрос
    html = requests.get(url).text
    #Находим колличество текстов
    songsCount, lastSearchIndex = searchInnerText(html, 'Всего текстов: ', '</th>', lastSearchIndex)
    songsCount=int(songsCount)
    
    
    if songsCount<=0:
        bot.send_message(msg_chat_id, "Тaких песен не нашли :(")
    else:
        if startindex==0:
            bot.send_message(msg_chat_id, "Всего найдено песен и исполнителей: {}".format(songsCount))
        k=min(startindex+max_songs_count_perpage, songsCount)
        inline_kb1 = types.InlineKeyboardMarkup()
        for i in range(k):
            songUrl, lastSearchIndex = searchInnerText(html, '<td><a href="', '">', lastSearchIndex)
            songName, lastSearchIndex = searchInnerText(html, '">', '</a></td>', lastSearchIndex)
            if i<startindex:
                continue
            #bot.send_message(msg_chat_id, songName)
            
            data="{}{}{}".format(btn_marker,op_showtext, link_shorter(siteurl+songUrl))
            #print(f'len(data)=[{len(data)}]')
            
            inline_btn_showlyrics = InlineKeyboardButton(
                "{}. {}".format(i+1, songName), 
                callback_data=data
            )
            inline_kb1.add(inline_btn_showlyrics) 
        
        if k != songsCount:
            inline_kb1.add(InlineKeyboardButton(
                "Следующие {} результатов".format(max_songs_count_perpage),
                callback_data="{}{} {} {}".format(btn_marker,op_next, k, link_shorter(url))
            ))
                
        bot.send_message(msg_chat_id, "Результаты поиска с {} по {}".format(startindex + 1, k), reply_markup=inline_kb1)
           
#==========================================================================
def ShowText(msg_chat_id, song_url):
    html = requests.get(song_url).text
    
     
    txt, xx = searchInnerText(html, '<p>', '</p>', html.find('<li role="presentation" class="active"><a href="#">Текст песни</a></li>'))
    txt = txt.replace('<br>', '')
    
    songname, xx = searchInnerText(html, '<h1>', 'текст песни', html.find('<a href="/browse/ru-YA.html" class="let btn btn-default">Я</a>'))
    
    link = link_shorter('https://music.yandex.ru/search?text=' + songname.replace(' ', '%20'))
    
    kb = types.InlineKeyboardMarkup()
    ya_button = types.InlineKeyboardButton(text="Яндекс музыка", url = link)
    kb.add(ya_button)
    
    
    bot.send_message(msg_chat_id, songname+"\n\n"+txt, reply_markup=kb)
            

def searchInnerText(txt, marker1, marker2, startSearchIndex):
    start1=txt.find(marker1, startSearchIndex) + len(marker1)
    start2=txt.find(marker2, start1)
    res = txt[start1:start2]
    return res, start2
    

def waytopf():
    topstart = (searchtext.find(s)) + 13
    topend = (searchtext.find('>', topstart)) - 2
    topway.append(searchtext[topstart:topend])
    #---
    nam = searchtext[topend+3:searchtext.find('</', topend+3)]
    topname.append(nam)
    print(topname)
#==========================================================================
#Here is the token for bot SongText @SongTexterbot
bot=telebot.TeleBot("1604429645:AAFbXQ3rx_a4MMV1LGCYghF2HmwD25J69pE")


mid = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
mid.row('🔎Найти песню🔎','❓Что я умею?❓', 'ℹ️О насℹ️')
#==========================================================================
#dp = Dispatcher(bot)

@bot.callback_query_handler(func=lambda c: True)# c.data and c.data.startswith(btn_marker))
def process_callback_btn(callback_query): #types.CallbackQuery
    # получить код операции
    callback_data=callback_query.data[len(btn_marker):]
    op_code=callback_data[0]
    callback_data = callback_data[1:]
    # определить параметры, включая URL
    # вызывать url, найти нужные данные в html
    # отобразитm кнопки
    if int(op_code) == op_next:
        # определить параметры, включая URL
        start_index = callback_data[1:callback_data.find(" ",2)]
        searchurl = callback_data[callback_data.find(start_index)+len(start_index)+1:] 
        # отобразитm кнопки
        searchSongsShowButtons(callback_query.message.chat.id, searchurl, int(start_index))
    if int(op_code) == op_showtext:
        # определить параметры, включая URL
        # отобразитm тtкст и кнопку TOP 20 b кнопку Yandex M
        ShowText(callback_query.message.chat.id, callback_data)
#==========================================================================
#def top20(url):
#    for i in range(5)
#=================================================================================================================================================
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я умею находить песни и их исполнителей по любому слову из названия! Проверь! Просто отправь мне свою любимую песню и я покажу тебе ее слова и дам ссылку на яндекс музыку.', reply_markup=mid)
      
    
@bot.message_handler(content_types=['text'])
def vibor(message):
    print(message)
    print(message.text)
    if message.text == '🔎Найти песню🔎':
        bot.send_message(message.chat.id, 'Отправь мне название песни или исполнителя')
    elif message.text == '❓Что я умею?❓':
        bot.send_message(message.chat.id, 'Я умею находить песни и их исполнителей по любому слову из названия! Проверь!', reply_markup=mid)
    elif message.text =='ℹ️О насℹ️':
        bot.send_message(message.chat.id, 'Бот был написан @Depost1497 11.03.2021', reply_markup=mid)
    else:
        #составляем поисковый url
        search_text = message.text.replace(' ', '+')
        url = siteurl+'/search/?s='+search_text
        searchSongsShowButtons(message.chat.id, url, 0)
    
    
#без остановки
bot.polling(none_stop=True, interval=0)