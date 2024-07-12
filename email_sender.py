import smtplib
from email.mime.text import MIMEText


SENDER_EMAIL = 'vacancy.notification@demomailtrap.com'


def send_email(subject, body, reciever_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = reciever_email

    try:
        with smtplib.SMTP('sandbox.smtp.mailtrap.io', 2525) as server:
            server.login('306e2f7d4d9c82', '5cb64a420b68da')
            server.sendmail(SENDER_EMAIL, [reciever_email], msg.as_string())
            print("Email sent successfully!")

    except Exception as e:
        print(e)


if __name__ == '__main__':
    send_email('test_subject', 'test_body', 'some.email@gmail.com')
