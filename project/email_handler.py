# libraries to be imported
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
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
email_cc = os.getenv("EMAIL_CC")


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
            em['CC'] = email_cc
            em['subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smpt:
                smpt.login(email_sender, email_password)
                smpt.sendmail(email_sender, email_receiver.split(
                    ";") + (email_cc.split(";") if email_cc else []), em.as_string())
                smpt.quit()
            print("Email was sent Successfully...")
        except Exception as ex:
            print(f'Exception Occured ! \n {ex}')

    def sendFile(self, file_path=None):
        print('Sending email...')
        try:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            subject = 'Email Attachment Automation with Python'
            em = MIMEMultipart('mixed')
            em['From'] = 'Contact <{sender}>'.format(sender=email_sender)
            em['To'] = email_receiver
            em['CC'] = 'sebastian_gvl@hotmail.com'
            em['subject'] = subject

            em_content = '<h4>Hello {email_sender},<br> This is a test email with attachment, send from python script to automate the process.</h4>\n'
            body = MIMEText(em_content, 'html')
            em.attach(body)

            with open(file_path, "rb") as attachment:
                p = MIMEApplication(attachment.read(), _subtype="pdf")
                p.add_header(
                    'Content-Disposition', "attachment; filename= %s" % file_path.split("\\")[-1])
                em.attach(p)
                attachment.close()

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as smpt:
                smpt.ehlo()
                smpt.login(email_sender, email_password)
                smpt.sendmail(email_sender, email_receiver.split(
                    ";") + (email_cc.split(";") if email_cc else []), em.as_string())
                smpt.quit()

            print("Email was sent Successfully...")
        except Exception as ex:
            print(f'Exception Occured ! \n {ex}')
