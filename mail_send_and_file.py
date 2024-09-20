import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv, dotenv_values 

# Загрузка переменных из .env файла
load_dotenv() 

# Данные для входа
app_name = os.getenv('name_app_gmail')
password = os.getenv('password_app_gmail')
sender = os.getenv('email_login_001')
recipients_1 = os.getenv('email_login_002')
recipients_2 = os.getenv('email_login_003')

subject = "Email Subject"
body = "This is the body of the text message"
recipients = [recipients_1, recipients_2]
attachments = ["name_file_1", "name_file_2"]  # Список файлов для вложения


def send_email(subject, body, sender, recipients, password, attachments):
    # Создание MIMEMultipart объекта для письма
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    # Добавление текста письма
    msg.attach(MIMEText(body, 'plain'))

    # Добавление вложений
    for attachment in attachments:
        try:
            with open(attachment, "rb") as file:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(attachment)}",
            )
            msg.attach(part)
        except Exception as e:
            print(f"Не удалось прикрепить файл {attachment}: {e}")
            continue

    # Подключение к SMTP-серверу Gmail и отправка письма
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, app_name) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())

    print("Message sent!")

# Вызов функции для отправки письма
send_email(subject, body, sender, recipients, password, attachments)
