from bs4 import BeautifulSoup
import re
import random
import requests
import datetime
from fake_useragent import UserAgent
import sqlite3


import telebot

import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 
TOKEN = os.getenv('TOKEN')
chat_id = os.getenv('chat_id')

bot = telebot.TeleBot(TOKEN)


ua = UserAgent()

headers = {
    'accept': 'application/json, text/plain, */*',
    'user-Agent': ua.google,
}
page = 0

while True:
    #url = f'https://s7.myfanstv.net/series/page/' + str(p)

    req = requests.get(str('https://s7.myfanstv.net/series/page/') + str(page), headers=headers).text

    soup = BeautifulSoup(req, 'lxml')

    title = soup.find_all("div", class_="field-title")
    title_1 = soup.find_all("div", class_="field-description")
    title_2 = soup.find_all("div", class_="field-description")

    connection = sqlite3.connect('my_database.db')

    cursor = connection.cursor() 
    
    try:
        cursor.execute('''      
        CREATE TABLE "serials" (
            "name"	TEXT NOT NULL,
            "date"	NUMERIC NOT NULL,
            "season"	INTEGER NOT NULL,
            "num"	INTEGER NOT NULL,
            "link"	TEXT,
            PRIMARY KEY("name","season","num")
        );
        ''')
    except:
        цуе = 0

    count_ok = 0
    count_bad = 0
    i=0
    
    if (len(title_1)):
        for el_1 in title_1:
            el = title[i].text + el_1.text
            [(name,sezon,serial)] = re.findall(r"(.+)\s(\d+)\s\w+\s(\d+)", el)
            print(title[i].text, el_1.text)
            i=+1
            link = el_1.find("a").get("href")
            g = datetime.datetime.now()
            try:
                cursor.execute('INSERT INTO serials (name, date, season, num, link) VALUES (?, ?, ?, ?, ?)', (name, g, sezon, serial, link) )
                count_ok+=1
                text = el
                
                #bot.send_message(chat_id, text, link)
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                count_bad+=1
            #raise
        print (count_bad, count_ok, page)

        connection.commit()

        connection.close()
        page += 1
        
    else:
        break
#document.querySelector('#pagination a:nth-last-child(n-1)')