import os
import smtplib
from email.mime.text import MIMEText


SENDER_EMAIL = 'vacancy.notification@demomailtrap.com'
RECEIVER_EMAIL = 'change.email.in.data.file@gmail.com'
PASSWORD = ''
SUBJECT = 'New vacancy on "{}"'


def read_email_data(f_path='email_data.txt'):
    """
    That file uses https://mailtrap.io/ SMTP server to send messages. You need a free account on mailtrap website.
    See more there: https://youtu.be/wDYADks8VBM?si=OLHW68y38FFIVaXZ
    Create in this repo file "email_data.txt" and fill it with data:
    password: password from mailtrap
    receiver_email: email.to.send@gmail.com
    """

    if os.path.isfile(f_path):
        with open(f_path, 'r') as file:
            lines = file.readlines()
            email_data = {line.split(':')[0].strip(): line.split(':')[1].strip() for line in lines}

            global RECEIVER_EMAIL, PASSWORD
            PASSWORD = email_data.get('password')
            RECEIVER_EMAIL = email_data.get('receiver_email')


# Get data from file
read_email_data()


def send_email(website, body):
    msg = MIMEText(body)
    msg['Subject'] = SUBJECT.format(website)
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP('live.smtp.mailtrap.io', 587) as server:
            server.starttls()
            server.login('api', PASSWORD)
            server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
            return True

    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    send_email('dou', 'test_body')
