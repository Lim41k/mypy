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
token = os.getenv('TOKEN')
chat_id = os.getenv('chat_id')

bot = telebot.TeleBot(token)

ua = UserAgent()

headers = {
    'accept': 'application/json, text/plain, */*',
    'user-Agent': ua.google,
}


url = 'https://s7.myfanstv.net/series/page/1/'

req = requests.get(url, headers=headers).text

soup = BeautifulSoup(req, 'lxml')


elements = soup.find_all("div", class_="serial-bottom")




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
    pass

count_ok = 0
count_bad = 0
g = datetime.datetime.now()

print('start', g)

for el in elements:
    el_1 = el.find("div", class_="field-title")
    el_2 = el.find("div", class_="field-description")
    link = el_2.find("a").get("href")
    el_3 = el_1.text + el_2.text
    [(name,sezon,serial)] = re.findall(r"(.+)\s(\d+)\s\w+\s(\d+)", el_3)
    names = name.strip()
    print(el_1.text + el_2.text)
  
    
    
    try:

        # read property updateRows
        query = cursor.execute(
            'INSERT INTO serials (name, date, season, num, link)' +
            ' VALUES (?, ?, ?, ?, ?) on CONFLICT (name, season, num) DO NOTHING;',
              (names, g, sezon, serial, link) 
              )
        count_ok+=query.rowcount
        text = names + link
        if query.rowcount == 1:
            bot.send_message(chat_id, text)
        else:
            pass

    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        count_bad+=1
    # #raise

print (f"Ошибок      {count_bad}")
print (f"Новые серии {count_ok}")
print('stop', g)

connection.commit()

connection.close()

