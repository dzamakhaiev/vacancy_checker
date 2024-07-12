import smtplib
from email.mime.text import MIMEText


SENDER_EMAIL = 'vacancy.notification@demomailtrap.com'
RECEIVER_EMAIL = 'some.email@gmail.com'
SUBJECT = 'New vacancy on "{}"'


def send_email(website, body):
    msg = MIMEText(body)
    msg['Subject'] = SUBJECT.format(website)
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP('sandbox.smtp.mailtrap.io', 2525) as server:
            server.login('306e2f7d4d9c82', '5cb64a420b68da')
            server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
            return True

    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    send_email('dou', 'test_body')
