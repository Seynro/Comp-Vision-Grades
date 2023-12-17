from email.message import EmailMessage
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def email_sender(email_receiver, subject, body, filename):
    email_sender = 'ada.statistics@gmail.com'
    email_password = 'hghw kdxb tytb gftk'

    # Создаем объект сообщения
    em = MIMEMultipart()
    em['From'] = email_sender 
    em['To'] = email_receiver 
    em['Subject'] = subject 

    # Добавляем тело письма (текст)
    em.attach(MIMEText(body, 'plain'))

    # Открываем файл изображения в двоичном режиме
    
    with open(filename, 'rb') as attachment:
        # Создаем объект MIMEBase и добавляем файл изображения
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    # Кодируем файл для отправки по электронной почте
    encoders.encode_base64(part)

    # Добавляем заголовок к части вложения
    part.add_header(
        'Content-Disposition',
        f'attachment; filename= Quiz.jpg',
    )

    # Добавляем вложение к сообщению
    em.attach(part)

    # Отправляем письмо
    ssl_context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl_context) as server:
        server.login(email_sender, email_password)
        server.send_message(em)
        print('Email sent successfully')


# filename = r"C:\Users\user\Desktop\Programs\Tap.az\inst.jpg"

# subject = 'Test for mail'

# body = f'''Dear test, Hope you are doing well. '''
# email_sender('samarau16878@ada.edu.az', subject, body, filename)
