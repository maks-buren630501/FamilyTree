import smtplib

from backend.core.additional import singleton
from backend.core.email.config import mail_auth


@singleton
class Mail:

    def __init__(self, gmail_user, gmail_password):
        try:
            self.user = gmail_user
            self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            self.server.ehlo()
            self.server.login(gmail_user, gmail_password)
        except Exception as e:
            print('error mail connection', e)
            exit()

    def send_message(self, to, text):
        self.server.sendmail(self.user, to, text)

    def __del__(self):
        self.server.close()


mail = Mail(mail_auth.user, mail_auth.password)
