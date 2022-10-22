# libraries to be imported
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
#from re import sub
import ssl
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

email_sender = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_PASSWORD")
email_receiver = os.getenv("EMAIL_RECEIVER")


class Email():
    def __init__(self):
        pass

    def send(self, message=None):
        print('Sending email...')
        try:
            subject = 'Email Automation with Python'
            body = "\n".join(["""
            This is a test email, send from python script to automate the process.   
            """, message])

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smpt:
                smpt.login(email_sender, email_password)
                smpt.sendmail(email_sender, email_receiver, em.as_string())
            print("Email was sent Successfully...")
        except Exception as ex:
            print(f'Exception Occured ! \n {ex}')

    # def sendFile(self, file_path=None):
