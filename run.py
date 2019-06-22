import config
import requests
import smtplib
import ssl
import getpass

# email objects
port = 587  # For starttls
smtp_server = "smtp.gmail.com"
context = ssl.create_default_context()
email = ''

# API request objects
base_currency = 'EUR'
response = ''


def run():
    global base_currency, response
    url = "https://api.exchangerate-api.com/v4/latest/" + base_currency
    send_request = requests.get(url)
    response = send_request.json()
    create_msg()
    send_email()


class Email:
    def __init__(self, sender_email, receiver_email, subject):
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.subject = subject

    def body(self, body):
        self.body = body
        self.message = f"""\
Subject: {self.subject}

{self.body}"""


def create_msg():
    global email
    email = Email(
        sender_email=config.sender_email,
        receiver_email=config.receiver_email,
        subject=f'오늘의 환율 ({base_currency}<->KRW): {response["rates"]["KRW"]}'
    )
    email.body((f"""
    Date: {response["date"]}
    Base: {base_currency}
    KRW: {response["rates"]["KRW"]}
    
    😇
    """))


def send_email():
    password = config.email_pwd
    create_msg()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(email.sender_email, password)
        server.sendmail(email.sender_email, email.receiver_email,
                        email.message.encode("utf8"))


run()
