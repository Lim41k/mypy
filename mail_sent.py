import smtplib
from email.mime.text import MIMEText
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

# Define the subject and body of the email.
subject = "Email Subject"
body = "This is the body of the text message"
recipients = [recipients_1, recipients_2]


def send_email(subject, body, sender, recipients, password):
    # Create a MIMEText object with the body of the email.
    msg = MIMEText(body)
    # Set the subject of the email.
    msg['Subject'] = subject
    # Set the sender's email.
    msg['From'] = sender
    # Join the list of recipients into a single string separated by commas.
    msg['To'] = ', '.join(recipients)
   
    # Connect to Gmail's SMTP server using SSL.
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, app_name) as smtp_server:
        # Login to the SMTP server using the sender's credentials.
        smtp_server.login(sender, password)
        # Send the email. The sendmail function requires the sender's email, the list of recipients, and the email message as a string.
        smtp_server.sendmail(sender, recipients, msg.as_string())
    # Print a message to console after successfully sending the email.
    print("Message sent!")

# Call the function to send the email.
send_email(subject, body, sender, recipients, password)