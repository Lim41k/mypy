import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
import datetime
import re
import sqlite3
import pytz  # Для работы с часовыми поясами

# Загрузка переменных из .env файла
load_dotenv()

# Данные для входа
username = os.getenv('email_login_003')
password = os.getenv('email_password_003_IMAP')

# Подключение к почтовому серверу через IMAP
mail = imaplib.IMAP4_SSL("imap.ukr.net")
mail.login(username, password)

# Выбор папки "Входящие"
mail.select("inbox")

# Поиск всех писем
status, messages = mail.search(None, "ALL")

# Преобразование списка номеров писем в массив
mail_ids = messages[0].split()

# Подключение к базе данных
conn = sqlite3.connect('emails.db')
cursor = conn.cursor()

# Создание таблицы для писем и вложений с уникальным ключом на дату
cursor.execute('''
CREATE TABLE IF NOT EXISTS emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    sender TEXT,
    date TEXT UNIQUE,
    body TEXT,
    attachment_filename TEXT,
    attachment BLOB
)
''')

# Определение локального часового пояса
local_tz = pytz.timezone('Europe/Kiev')  # Укажите ваш локальный часовой пояс

# Парсинг последних 5 писем
for i in range(1, 11):  # Парсим 5 последних писем
    mail_id = mail_ids[-i]
    
    # Получение данных о письме
    status, msg_data = mail.fetch(mail_id, "(RFC822)")
    
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            # Парсинг байтов сообщения
            msg = email.message_from_bytes(response_part[1])
            
            # Декодирование темы письма
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
            
            # Декодирование отправителя
            from_ = msg.get("From")
            
            # Получение и форматирование даты
            date_ = msg.get("Date")
            date_ = re.sub(r'\s+\(.*\)$', '', date_)
            email_date = datetime.datetime.strptime(date_, '%a, %d %b %Y %H:%M:%S %z')

            # Преобразование даты в локальный часовой пояс
            local_date = email_date.astimezone(local_tz)
            formatted_date = local_date.strftime('%Y-%m-%d %H:%M:%S')

            # Обработка тела письма
            body = ""
            attachments = []

            # Если письмо содержит несколько частей, парсим каждую
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if "attachment" in content_disposition:
                        # Если часть письма - это вложение, сохраняем его
                        filename = part.get_filename()
                        if filename:
                            filename = decode_header(filename)[0][0]
                            if isinstance(filename, bytes):
                                filename = filename.decode(encoding if encoding else "utf-8")
                            
                            # Получаем бинарное содержимое вложения
                            # attachment_data = part.get_payload(decode=False)
                            # print("++++++++++++++++++")
                            # print(attachment_data)
                            # print("++++++++++++++++++")
                            attachment_data = part.get_payload(decode=True)
                            # print("++++++++++++++++++")
                            # print(attachment_data)
                            # print("++++++++++++++++++")
                            attachments.append((filename, attachment_data))
                    elif content_type == "text/plain" and "attachment" not in content_disposition:
                        # Если часть письма - это текст
                        body = part.get_payload(decode=True).decode("utf-8")
            else:
                # Если письмо не содержит нескольких частей
                body = msg.get_payload(decode=True).decode("utf-8")

            # Вывод содержимого письма в терминал
            print("="*100)
            print(f"Тема: {subject}")
            print(f"Отправитель: {from_}")
            print(f"Дата: {formatted_date}")
            print(f"Тело письма:\n{body}")
            
            if attachments:
                for filename, _ in attachments:
                    print(f"Вложение: {filename}")
            else:
                print("Вложений нет.")
            print("="*100)

            # Сохранение письма и вложений в базу данных
            try:
                if not attachments:
                    # Сохранение письма без вложений
                    cursor.execute('''
                    INSERT INTO emails (subject, sender, date, body, attachment_filename, attachment) 
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (subject, from_, formatted_date, body, None, None))
                else:
                    # Сохранение письма с вложениями в бинарном виде
                    for filename, attachment_data in attachments:
                        cursor.execute('''
                        INSERT INTO emails (subject, sender, date, body, attachment_filename, attachment) 
                        VALUES (?, ?, ?, ?, ?, ?)
                        ''', (subject, from_, formatted_date, body, filename, attachment_data))
                print("Письмо и вложения сохранены в базе данных.")
            except sqlite3.IntegrityError:
                print(f"Письмо с датой {formatted_date} уже существует в базе данных и не было добавлено.")
            print("="*100)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
mail.logout()
