from multiprocessing import Process
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from html import escape

from config import MAIL_DEFAULT_SENDER, MAIL_PASSWORD, MAIL_SERVER, MAIL_USERNAME, MAIL_PORT, MAIL_ASYNC


def send_verify_email(name: str, receiver: str, token: str):
    def _send(message):
        with smtplib.SMTP(MAIL_SERVER, int(MAIL_PORT),  timeout=5) as smtp:
            smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
            smtp.sendmail(MAIL_DEFAULT_SENDER, receiver, message.as_string())
    mail_msg = f"你好，感谢注册WMCTF，输入以下代码验证你的账号：{token}<br/>Hello, thanks for register, verify your account by code: {token}"
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = f"WMCTF <{MAIL_DEFAULT_SENDER}>"
    message['To'] = f"{name} <{receiver}>"

    subject = "Verify your account"
    message['Subject'] = Header(subject, 'utf-8')
    if MAIL_ASYNC:
        Process(target=_send, args=(message, )).start()
    else:
        _send(message)

def send_forget_email(name: str, receiver: str, password: str):
    def _send(message):
        with smtplib.SMTP(MAIL_SERVER, int(MAIL_PORT),  timeout=5) as smtp:
            smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
            smtp.sendmail(MAIL_DEFAULT_SENDER, receiver, message.as_string())
    mail_msg = f"你好，这是你的队伍名和密码，请牢记：<br/>This is your teamname and password, do not forget it again<br/>{escape(name)}<br/>{escape(password)}"
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = f"WMCTF <{MAIL_DEFAULT_SENDER}>"
    message['To'] = f"{name} <{receiver}>"

    subject = "Remember your info"
    message['Subject'] = Header(subject, 'utf-8')
    Process(target=_send, args=(message, )).start()
    if bool(MAIL_ASYNC):
        Process(target=_send, args=(message, )).start()
    else:
        _send(message)
