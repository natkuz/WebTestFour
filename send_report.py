import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
import yaml
import datetime as DT

with open('testdata.yaml', encoding='utf-8') as f:
    testdata = yaml.safe_load(f)

now = DT.datetime.now(DT.timezone.utc).astimezone()
time_format = "%Y-%m-%d %H:%M:%S"
report_name = f"report {now:{time_format}}.xml"

# данные для отправки письма
sender_email = testdata.get('from_addr_report')
recipient_email = testdata.get('to_addr_report')
subject = report_name
message_body = "Text"
file_name = 'log.txt'

# Создание объекта MIMEMultipart
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = subject

# Добавление текста сообщения
msg.attach(MIMEText(message_body, 'plain'))

# Добавление файла во вложение
with open(file_name, 'rb') as f:
    attach = MIMEBase('application', 'octet-stream')
    attach.set_payload(f.read())
    encoders.encode_base64(attach)
    attach.add_header('Content-Disposition', f'attachment; filename = {file_name}')
    msg.attach(attach)

# Ввод пароля для почты отправителя
password = testdata.get('mail_password')

# настройка smtp-сервера mail.ru
smtp_server = 'smtp.mail.ru'
smtp_port = 587

# Создание объекта smtp
server = smtplib.SMTP(smtp_server, smtp_port)
try:
    # установка соединения
    server.starttls()  # включение шифрованного соединения
    server.login(sender_email, password)  # вход в почтовый аккаунт
    # отправка письма
    server.sendmail(sender_email, recipient_email, msg.as_string())
    print("Report send")
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    # Завершение соединения с SMTP_сервером
    server.quit()
